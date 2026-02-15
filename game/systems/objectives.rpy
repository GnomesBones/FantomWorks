# game/systems/objectives.rpy
# Objective + Quest Manager
#
# Purpose:
# - One pinned objective shown on HUD.
# - Multiple quests tracked in a log (grouped by type).
# - Steps can be mandatory or optional.
# - Completing a step can auto-advance to the next step in the same quest.
#
# Quest types supported:
# - investigative
# - character_arc
# - player_progression
# - ghost_arc
#
# Notes:
# - Keep quest definitions in this file.
# - Call obj_pin(step_id) to set the HUD objective.
# - Call obj_complete(step_id) when an action is done (post, sleep, read replies, etc).
# - Use obj_can_leave_house() to gate map travel.
# - Use obj_app_enabled("notreddit") to gate laptop apps.

##############################################################################
# 1) Defaults (saved state)
##############################################################################

default pinned_step_id = None

# Quests the player has been assigned / discovered
default discovered_quests = set()

# Step completion state:
# { "quest_id.step_id": True/False }
default step_done = {}

# Optional: keep a short log of completed steps for UI/journal
default objective_history = []

# App gates for current pinned objective (computed on pin)
default apps_enabled = {
    "notreddit": False,
    "inneed": False,
    "replies": False,
    "schedule": False,
    "utoob": False,
    "webdive": False,
}

# Travel gate for current pinned objective
default can_leave_house = False


# Editing:
# - Add new quests here.
# - Add new step ids inside steps lists.
# - If a step should drive the HUD, set "pin": True.


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

init python:

    QUEST_TYPES = ["investigative", "character_arc", "player_progression", "ghost_arc", "job_quest"]

    # Helper: build full step id
    def _sid(qid, step_id):
        return qid + "." + step_id

    def obj_discover_quest(quest_id):
        if quest_id in QUESTS:
            store.discovered_quests.add(quest_id)
            return True
        return False

    def obj_is_discovered(quest_id):
        return quest_id in store.discovered_quests


    QUESTS = {

        # ==============================================================
        # PLAYER PROGRESSION: ONBOARDING / RECRUITMENT ARC
        # ==============================================================

        "prog.onboarding": {
            "type": "player_progression",
            "title": "First Steps",
            "description": "Set up the work, get eyes on it, and wait for the world to blink back.",
            "steps": [

                {
                    "id": "make_post",
                    "text": "Make a NotReddit post.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["notreddit"],
                    "auto_next": _sid("prog.onboarding", "sleep_1"),
                },

                {
                    "id": "sleep_1",
                    "text": "Sleep.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": [],
                    "auto_next": _sid("prog.onboarding", "wait_replies_1"),
                },

                {
                    "id": "wait_replies_1",
                    "text": "Wait for replies.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["notreddit"],
                    "auto_next": _sid("prog.onboarding", "check_inneed"),
                },

                {
                    "id": "free_reign_house",
                    "text": "Free time.",
                    "mandatory": False,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["notreddit", "inneed", "webdive", "utoob", "schedule"],
                    "auto_next": _sid("prog.onboarding", "read_replies_optional"),
                },

                {
                    "id": "read_replies_optional",
                    "text": "Read replies. Optional for now.",
                    "mandatory": False,
                    "pin": False,
                    "can_leave_house": False,
                    "enable_apps": ["replies", "notreddit"],
                    "auto_next": None,
                },

                {
                    "id": "read_replies_mandatory",
                    "text": "Read replies.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["replies"],
                    "auto_next": _sid("prog.onboarding", "set_meetup"),
                },

                {
                    "id": "set_meetup",
                    "text": "Set the meet up.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["schedule", "replies"],
                    "auto_next": _sid("prog.onboarding", "sleep_2"),
                },

                {
                    "id": "sleep_2",
                    "text": "Sleep.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": [],
                    "auto_next": _sid("prog.onboarding", "read_replies_mandatory_2"),
                },

                {
                    "id": "read_replies_mandatory_2",
                    "text": "Read replies.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["replies"],
                    "auto_next": _sid("prog.onboarding", "meet_team"),
                },

                {
                    "id": "meet_team",
                    "text": "Meet the team.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": True,
                    "enable_apps": [],
                    "auto_next": None,
                },
            ],
        },

        # ==============================================================
        # INVESTIGATIVE: FIRST CASE HOOK (placeholder example)
        # ==============================================================

        "inv.case_01": {
            "type": "investigative",
            "title": "Case 01: The First Call",
            "description": "A job lands. Something is off. Evidence wants collecting.",
            "steps": [
                {
                    "id": "accept_job",
                    "text": "Accept the first job from InNeed.",
                    "mandatory": True,
                    "pin": False,
                    "can_leave_house": False,
                    "enable_apps": ["inneed"],
                    "auto_next": None,
                },
                {
                    "id": "pack_gear",
                    "text": "Pack gear for the job.",
                    "mandatory": True,
                    "pin": False,
                    "can_leave_house": False,
                    "enable_apps": [],
                    "auto_next": None,
                },
            ],
        },

        # ==============================================================
        # GHOST ARC: BACKY MOOBY / BOBBY MACKEY INSPIRED (placeholder)
        # ==============================================================

        "ghost.backy_mooby": {
            "type": "ghost_arc",
            "title": "Backy Mooby's Music World",
            "description": "The building keeps its own receipts.",
            "steps": [
                {
                    "id": "arrive",
                    "text": "Arrive at Backy Mooby's.",
                    "mandatory": True,
                    "pin": False,
                    "can_leave_house": True,
                    "enable_apps": [],
                    "auto_next": None,
                },
            ],
        },

        # ==============================================================
        # PLAYER PROGRESSION: ONBOARDING / RECRUITMENT ARC
        # ==============================================================

        "job.intro": {
            "type": "job_quest",
            "title": "Odd Jobs",
            "description": "Save up some money to buy new equipment.",
            "steps": [
                {
                    "id": "check_inneed",
                    "text": "Look at InNeed for a job.",
                    "mandatory": True,
                    "pin": True,
                    "can_leave_house": False,
                    "enable_apps": ["inneed"],
                    "auto_next": _sid("prog.onboarding", "free_reign_house"),
                },
            ],
        },
    }

##############################################################################
# 3) Indexes for fast lookup
##############################################################################
# Built once at init.

init python:

    STEP_INDEX = {}     # full_step_id -> step dict
    QUEST_INDEX = {}    # full_step_id -> quest_id

    def _build_indexes():
        STEP_INDEX.clear()
        QUEST_INDEX.clear()

        for qid, q in QUESTS.items():
            for s in q.get("steps", []):
                full = _sid(qid, s["id"])
                STEP_INDEX[full] = s
                QUEST_INDEX[full] = qid

    _build_indexes()


##############################################################################
# 4) Core API
##############################################################################

init python:

    def obj_exists(full_step_id):
        return full_step_id in STEP_INDEX

    def obj_is_done(full_step_id):
        return bool(step_done.get(full_step_id, False))

    def obj_mark_done(full_step_id):
        step_done[full_step_id] = True

    def obj_mark_not_done(full_step_id):
        step_done[full_step_id] = False

    def obj_current_text():
        """
        Text shown on HUD for current pinned objective.
        """
        if pinned_step_id is None:
            return ""
        if not obj_exists(pinned_step_id):
            return ""
        return STEP_INDEX[pinned_step_id].get("text", "")

    def obj_app_enabled(app_key):
        """
        Used by laptop UI to enable/disable apps.
        """
        return bool(apps_enabled.get(app_key, False))

    def obj_can_leave_house():
        """
        Used by map/travel gating.
        """
        return bool(can_leave_house)

    def _apply_gates_for_step(full_step_id):
        """
        Applies gates (apps and travel) based on the pinned step.
        """
        global can_leave_house

        # Reset app gates
        for k in list(apps_enabled.keys()):
            apps_enabled[k] = False

        can_leave_house = False

        if full_step_id is None:
            return
        if not obj_exists(full_step_id):
            return

        s = STEP_INDEX[full_step_id]
        can_leave_house = bool(s.get("can_leave_house", False))

        for a in s.get("enable_apps", []):
            if a in apps_enabled:
                apps_enabled[a] = True

    def obj_pin(full_step_id):
        """
        Pins an objective step to HUD and applies gates.
        """
        global pinned_step_id

        if full_step_id is not None and not obj_exists(full_step_id):
            pinned_step_id = None
            _apply_gates_for_step(None)
            return False

        pinned_step_id = full_step_id
        _apply_gates_for_step(full_step_id)
        return True

    def obj_pin_first_in_quest(quest_id):
        """
        Pins the first incomplete pinned step in a quest.
        If none are marked pin=True, pins the first incomplete mandatory step.
        """
        if quest_id not in QUESTS:
            return False

        steps = QUESTS[quest_id].get("steps", [])

        # Prefer steps explicitly flagged as pin=True
        for s in steps:
            full = _sid(quest_id, s["id"])
            if not obj_is_done(full) and bool(s.get("pin", False)):
                return obj_pin(full)

        # Otherwise prefer first incomplete mandatory
        for s in steps:
            full = _sid(quest_id, s["id"])
            if not obj_is_done(full) and bool(s.get("mandatory", True)):
                return obj_pin(full)

        # Otherwise any incomplete
        for s in steps:
            full = _sid(quest_id, s["id"])
            if not obj_is_done(full):
                return obj_pin(full)

        return False

    def obj_start_quest(quest_id):
        """
        Starts a quest by pinning the first appropriate step.
        """
        return obj_pin_first_in_quest(quest_id)

    def obj_complete(full_step_id=None, play_fx=True):
        """
        Completes a step. If full_step_id is None, completes pinned step.
        Auto-advances if auto_next is defined.
        If play_fx=True, calls objective complete animation if available.
        """
        global pinned_step_id

        sid = full_step_id if full_step_id is not None else pinned_step_id
        if sid is None:
            return False
        if not obj_exists(sid):
            return False
        if obj_is_done(sid):
            return False

        obj_mark_done(sid)

        # Add to history
        txt = STEP_INDEX[sid].get("text", "")
        if txt:
            objective_history.append(txt)

        # Optional completion FX hook (if function exists in store)
        if play_fx:
            try:
                # If hud.rpy defines play_objective_complete_fx
                renpy.call_in_new_context("objective_complete_fx_call", txt)
            except:
                pass

        # Auto-advance to next step if defined
        nxt = STEP_INDEX[sid].get("auto_next", None)
        if nxt is not None and obj_exists(nxt):
            obj_pin(nxt)
        else:
            # If completed step was pinned, try to pin next in same quest
            if sid == pinned_step_id:
                qid = QUEST_INDEX.get(sid, None)
                if qid is not None:
                    obj_pin_first_in_quest(qid)

        return True


##############################################################################
# 5) Quest log accessors (for pause menu / journal)
##############################################################################

init python:

    def obj_list_quests_by_type(qtype):
        """
        Returns quest_ids for a given type.
        """
        if qtype not in QUEST_TYPES:
            return []
        out = []
        for qid, q in QUESTS.items():
            if q.get("type") == qtype:
                out.append(qid)
        return out

    def obj_quest_progress(quest_id):
        """
        Returns (done_count, total_count, mandatory_remaining_count)
        """
        if quest_id not in QUESTS:
            return (0, 0, 0)

        steps = QUESTS[quest_id].get("steps", [])
        total = len(steps)
        done = 0
        mandatory_remaining = 0

        for s in steps:
            full = _sid(quest_id, s["id"])
            if obj_is_done(full):
                done += 1
            else:
                if bool(s.get("mandatory", True)):
                    mandatory_remaining += 1

        return (done, total, mandatory_remaining)

    def obj_quest_steps(quest_id):
        """
        Returns list of dicts: {full_id, text, done, mandatory}
        """
        if quest_id not in QUESTS:
            return []

        out = []
        for s in QUESTS[quest_id].get("steps", []):
            full = _sid(quest_id, s["id"])
            out.append({
                "full_id": full,
                "text": s.get("text", ""),
                "done": obj_is_done(full),
                "mandatory": bool(s.get("mandatory", True)),
            })
        return out

    def obj_find_pinned_step_info():
        """
        Returns dict for pinned step, or None.
        """
        if pinned_step_id is None:
            return None
        if not obj_exists(pinned_step_id):
            return None

        qid = QUEST_INDEX.get(pinned_step_id, None)
        step = STEP_INDEX[pinned_step_id]
        return {
            "full_id": pinned_step_id,
            "quest_id": qid,
            "text": step.get("text", ""),
            "mandatory": bool(step.get("mandatory", True)),
            "type": QUESTS[qid].get("type") if qid in QUESTS else None,
        }


    def obj_can_sleep():
        """
        Allow sleep only when the currently pinned objective is a sleep step.
        """
        sid = getattr(store, "pinned_step_id", None)
        if not sid:
            return False

        # Must exist and not already be done.
        if not obj_exists(sid) or obj_is_done(sid):
            return False

        # Our sleep steps in your quest are named sleep_1, sleep_2, etc.
        step = STEP_INDEX[sid]
        step_id = step.get("id", "")
        return step_id.startswith("sleep")

    def obj_next_step_text_for_quest(quest_id):
        """
        Returns the next step text for a quest (mandatory first, then any incomplete).
        Returns None if quest is complete.
        """
        if quest_id not in QUESTS:
            return None

        steps = QUESTS[quest_id].get("steps", [])

        # mandatory first
        for s in steps:
            full = _sid(quest_id, s["id"])
            if not obj_is_done(full) and bool(s.get("mandatory", True)):
                return s.get("text", "")

        # then any incomplete
        for s in steps:
            full = _sid(quest_id, s["id"])
            if not obj_is_done(full):
                return s.get("text", "")

        return None


    def obj_list_other_active_quests(max_per_type=3):
        """
        Returns a dict keyed by quest type, each value is a list of display rows:
        { "job_quest": [(title, next_text), ...], "investigative": [...], ... }

        "Active" here means: it has an incomplete step AND it's not the quest
        containing the currently pinned objective.
        """
        pinned_qid = QUEST_INDEX.get(store.pinned_step_id, None)

        buckets = { t: [] for t in QUEST_TYPES }

        for qid, q in QUESTS.items():
            if qid == pinned_qid:
                continue
            
            if not obj_is_discovered(qid):
                continue

            qtype = q.get("type", None)
            if qtype not in buckets:
                continue

            nxt = obj_next_step_text_for_quest(qid)
            if not nxt:
                continue

            title = q.get("title", qid)
            buckets[qtype].append((title, nxt))

        # Optional: limit spam
        if max_per_type is not None:
            for t in list(buckets.keys()):
                buckets[t] = buckets[t][:int(max_per_type)]

        return buckets


##############################################################################
# 6) Optional: Completion FX bridge label
##############################################################################
# This calls the HUD fx screen without importing HUD here.
# If a HUD screen isn't ready, nothing breaks.

label objective_complete_fx_call(text_to_show=""):
    # If a HUD helper exists, call it. Otherwise silently return.
    if renpy.has_label("objective_complete_fx_show"):
        call objective_complete_fx_show(text_to_show)
    return


##############################################################################
# 7) Optional: Start label (called once at beginning)
##############################################################################

label objectives_begin:
    # Start the onboarding quest and pin its first step
    $ obj_start_quest("prog.onboarding")
    return
