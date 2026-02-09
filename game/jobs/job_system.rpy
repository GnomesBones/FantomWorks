# jobs/job_system.rpy
# Generic job engine + persistent state for Nowhere, KY.
# Drop into game/jobs/. Ren'Py auto-loads .rpy files.

init -2 python:
    import random

    def _nj_default_state():
        return {
            "rep": {  # reputation per job
                "cleaning": 0,
                "landscaping": 0,
                "delivery": 0,
                "nursing": 0,
                "creative": 0,
            },
            "mastery": {  # lightweight mastery exp
                "cleaning": 0,
                "landscaping": 0,
                "delivery": 0,
                "nursing": 0,
                "creative": 0,
            },
            "lore_found": [],     # list[str]
            "threads": {},        # thread_id -> progress index
            "shift_history": [],  # list of shift ids completed
        }

    def nj_state():
        if not hasattr(persistent, "nowhere_jobs") or not isinstance(persistent.nowhere_jobs, dict):
            persistent.nowhere_jobs = _nj_default_state()
        # backfill keys if older save:
        d = persistent.nowhere_jobs
        for k, v in _nj_default_state().items():
            if k not in d:
                d[k] = v
        return d

    # --- Pay / rep tuning
    PAY_TABLE = {
        "cleaning":   [15, 25, 40, 60],
        "landscaping":[15, 25, 40, 60],
        "delivery":   [12, 20, 35, 55],
        "nursing":    [14, 22, 38, 58],
        "creative":   [10, 18, 30, 50],
    }
    REP_TABLE = {
        "success": 2,
        "fail": -1,
    }

    # --- Lore threads: order matters
    LORE_THREADS = {
        "founding_date_glitch": ["flyer_1987", "laundry_tag_1987", "park_banner_1987", "archive_gap"],
        "address_echo": ["receipt_oldtown_address", "gps_deadend_4th", "double_street_sign", "mailroom_blacklist"],
        "the_symbol": ["symbol_on_glove", "symbol_in_root", "symbol_on_stamp", "symbol_requested_logo"],
    }

    def nj_advance_threads(found_ids):
        st = nj_state()
        for thread_id, steps in LORE_THREADS.items():
            idx = st["threads"].get(thread_id, 0)
            while idx < len(steps) and steps[idx] in st["lore_found"]:
                idx += 1
            # if we just found the next step, progress will auto-catch up
            st["threads"][thread_id] = idx

    # --- Modifiers: tiny rules that keep shifts fresh
    # apply(job_state) may mutate job_state in-place.
    def _mod_short_timer(job_state):
        job_state["time_limit"] = max(5.0, job_state.get("time_limit", 20.0) * 0.75)

    def _mod_double_pay(job_state):
        job_state["pay_mult"] = job_state.get("pay_mult", 1.0) * 2.0
        job_state["risk_mult"] = job_state.get("risk_mult", 1.0) * 1.25

    def _mod_distraction(job_state):
        job_state["distraction_chance"] = min(0.75, job_state.get("distraction_chance", 0.15) + 0.20)

    JOB_MODIFIERS = {
        "short_timer": {"name": "Short Timer", "apply": _mod_short_timer},
        "double_pay": {"name": "Double Pay", "apply": _mod_double_pay},
        "distraction": {"name": "Distractions", "apply": _mod_distraction},
    }

    def pick_modifier(allowed_ids=None):
        if not allowed_ids:
            return None
        ids = [mid for mid in allowed_ids if mid in JOB_MODIFIERS]
        if not ids:
            return None
        # low chance of "no modifier" even if allowed
        if random.random() < 0.25:
            return None
        return random.choice(ids)

    # --- Shift picking helpers
    def _filter_unplayed(shifts):
        st = nj_state()
        played = set(st["shift_history"])
        unplayed = [s for s in shifts if s.get("id") not in played]
        return unplayed if unplayed else shifts

    def _difficulty_index(difficulty):
        # clamp 1..4
        return max(1, min(4, int(difficulty))) - 1

    def _base_pay(job_id, difficulty):
        idx = _difficulty_index(difficulty)
        return PAY_TABLE.get(job_id, [10, 15, 25, 40])[idx]

    def _apply_reward(job_id, success, difficulty, pay_mult=1.0):
        st = nj_state()
        pay = int(round(_base_pay(job_id, difficulty) * pay_mult))
        rep_delta = REP_TABLE["success"] if success else REP_TABLE["fail"]
        st["rep"][job_id] = st["rep"].get(job_id, 0) + rep_delta
        st["mastery"][job_id] = st["mastery"].get(job_id, 0) + (3 if success else 1)
        return pay, rep_delta

    # --- Main entry point
    def run_job(job_id, difficulty=1):
        """
        Runs one shift of a job.
        Returns dict:
          success: bool
          pay: int
          rep_delta: int
          lore_hits: list[str]
          modifier_id: str|None
          shift_id: str
          notes: list[str]
        """
        from store import renpy

        # Import content lists (defined in job_content.rpy)
        from store import CLEANING_SHIFTS, LANDSCAPING_SHIFTS, DELIVERY_SHIFTS, NURSING_SHIFTS, CREATIVE_SHIFTS

        pools = {
            "cleaning": CLEANING_SHIFTS,
            "landscaping": LANDSCAPING_SHIFTS,
            "delivery": DELIVERY_SHIFTS,
            "nursing": NURSING_SHIFTS,
            "creative": CREATIVE_SHIFTS,
        }
        shifts = pools.get(job_id, [])
        if not shifts:
            return {"success": False, "pay": 0, "rep_delta": 0, "lore_hits": [], "modifier_id": None, "shift_id": "none", "notes": ["No shifts configured."]}

        # prefer unplayed for variety
        choice_pool = _filter_unplayed(shifts)
        shift = random.choice(choice_pool)

        job_state = {
            "job_id": job_id,
            "difficulty": int(difficulty),
            "shift": shift,
            "time_limit": shift.get("time_limit", 20.0),
            "pay_mult": 1.0,
            "risk_mult": 1.0,
            "distraction_chance": 0.15,
        }

        modifier_id = pick_modifier(shift.get("mods"))
        if modifier_id:
            JOB_MODIFIERS[modifier_id]["apply"](job_state)

        # Dispatch to the right minigame screen/label
        # Each job file defines a label: job_<id>_play(job_state) that returns success, lore_hits, notes.
        renpy.call_in_new_context("job_dispatch_play", job_state)

        # job_dispatch_play stores result in _return
        result = renpy.get_return_stack()[-1] if renpy.get_return_stack() else None
        if isinstance(result, dict) and "success" in result:
            success = result["success"]
            lore_hits = result.get("lore_hits", [])
            notes = result.get("notes", [])
        else:
            # fallback if something weird happens
            success = False
            lore_hits = []
            notes = ["(Shift ended unexpectedly.)"]

        pay, rep_delta = _apply_reward(job_id, success, difficulty, pay_mult=job_state.get("pay_mult", 1.0))

        # persist history + lore
        st = nj_state()
        shift_id = shift.get("id", "unknown_shift")
        st["shift_history"].append(shift_id)

        new_lore = []
        for lid in lore_hits:
            if lid not in st["lore_found"]:
                st["lore_found"].append(lid)
                new_lore.append(lid)
        nj_advance_threads(new_lore)

        return {
            "success": success,
            "pay": pay,
            "rep_delta": rep_delta,
            "lore_hits": new_lore,
            "modifier_id": modifier_id,
            "shift_id": shift_id,
            "notes": notes,
        }


# --- A dispatch label so each job can be swapped without changing engine code.
label job_dispatch_play(job_state):
    $ job_id = job_state["job_id"]
    if job_id == "cleaning":
        call job_cleaning_play(job_state)
        return _return
    elif job_id == "landscaping":
        call job_landscaping_play(job_state)
        return _return
    elif job_id == "delivery":
        call job_delivery_play(job_state)
        return _return
    elif job_id == "nursing":
        call job_nursing_play(job_state)
        return _return
    elif job_id == "creative":
        call job_creative_play(job_state)
        return _return
    else:
        return {"success": False, "lore_hits": [], "notes": ["Unknown job id: %s" % job_id]}


# --- Dev test menu (jump here during development)
label jobs_debug_menu:
    menu:
        "Run Cleaning":
            $ r = run_job("cleaning", difficulty=1)
            "[r]"
            jump jobs_debug_menu
        "Run Landscaping":
            $ r = run_job("landscaping", difficulty=1)
            "[r]"
            jump jobs_debug_menu
        "Run Delivery":
            $ r = run_job("delivery", difficulty=1)
            "[r]"
            jump jobs_debug_menu
        "Run Nursing Home":
            $ r = run_job("nursing", difficulty=1)
            "[r]"
            jump jobs_debug_menu
        "Run Creative Contract":
            $ r = run_job("creative", difficulty=1)
            "[r]"
            jump jobs_debug_menu
        "View Lore Progress":
            $ st = nj_state()
            "Lore Found: [len(st['lore_found'])]"
            "Threads: [st['threads']]"
            jump jobs_debug_menu
        "Exit":
            return
