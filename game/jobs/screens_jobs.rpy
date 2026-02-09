# jobs/screens_jobs.rpy
# Reusable minigame screens.
# All screens are designed to be "content-driven" from job_state["shift"].

init -2 python:
    import random
    from store import renpy

    # --- Utility: pick one lore hit from a shift's lore list (with a chance)
    def maybe_lore(shift, chance=0.35):
        lore = shift.get("lore", [])
        if lore and random.random() < chance:
            return random.choice(lore)
        return None


# -----------------------------
# Cleaning: Hidden Object Search
# -----------------------------
screen mg_hidden_object(job_state):
    default found = set()
    default start_t = renpy.get_time()
    default time_limit = job_state.get("time_limit", 20.0)

    $ shift = job_state["shift"]
    $ items = shift.get("items", [])  # list of {name, x,y,w,h}
    $ title = shift.get("title", "Cleaning Shift")

    tag minigame

    add shift.get("bg", Solid("#111"))

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text title
        text "Find: [len(items)-len(found)] items"
        $ remaining = max(0.0, time_limit - (renpy.get_time() - start_t))
        text "Time: [remaining:.1f]"

    # Clickable hotspots
    for it in items:
        if it["name"] in found:
            continue
        button:
            xpos it.get("x", 0)
            ypos it.get("y", 0)
            xsize it.get("w", 60)
            ysize it.get("h", 40)
            background None
            action SetScreenVariable("found", found | {it["name"]})

    # Optional distraction popup
    if random.random() < job_state.get("distraction_chance", 0.15):
        frame:
            xalign 0.5
            yalign 0.25
            padding (18, 14)
            text shift.get("distraction_text", "Your phone buzzes with a notification you don't remember subscribing to.")

    timer 0.1 repeat True action If(
        (renpy.get_time() - start_t) >= time_limit,
        true=Return({"success": False, "found": list(found)}),
        false=NullAction()
    )

    # Win condition
    if len(found) >= len(items) and len(items) > 0:
        timer 0.1 action Return({"success": True, "found": list(found)})


# -----------------------------
# Landscaping: Anomaly Spotting
# -----------------------------
screen mg_anomaly_spot(job_state):
    default found = set()
    default start_t = renpy.get_time()
    default time_limit = job_state.get("time_limit", 18.0)

    $ shift = job_state["shift"]
    $ anomalies = shift.get("anomalies", [])  # list of {name, x,y,w,h}
    $ title = shift.get("title", "Landscaping Shift")

    tag minigame

    add shift.get("bg", Solid("#0b1a10"))

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text title
        text "Spot: [len(anomalies)-len(found)] anomalies"
        $ remaining = max(0.0, time_limit - (renpy.get_time() - start_t))
        text "Time: [remaining:.1f]"

    for a in anomalies:
        if a["name"] in found:
            continue
        button:
            xpos a.get("x", 0)
            ypos a.get("y", 0)
            xsize a.get("w", 60)
            ysize a.get("h", 40)
            background None
            action SetScreenVariable("found", found | {a["name"]})

    timer 0.1 repeat True action If(
        (renpy.get_time() - start_t) >= time_limit,
        true=Return({"success": False, "found": list(found)}),
        false=NullAction()
    )

    if len(found) >= len(anomalies) and len(anomalies) > 0:
        timer 0.1 action Return({"success": True, "found": list(found)})


# -----------------------------
# Delivery: Reaction Window
# -----------------------------
screen mg_reaction_window(job_state):
    default score = 0
    default rounds = 0
    default target_rounds = job_state["shift"].get("rounds", 6)
    default waiting = True
    default prompt_t = renpy.get_time()
    default window = job_state["shift"].get("window", 0.75)  # seconds
    default min_wait = job_state["shift"].get("min_wait", 0.7)
    default max_wait = job_state["shift"].get("max_wait", 2.2)
    default next_wait = renpy.random.uniform(min_wait, max_wait)

    $ shift = job_state["shift"]
    $ title = shift.get("title", "Courier Shift")

    tag minigame

    add shift.get("bg", Solid("#101018"))

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text title
        text "Stops cleared: [score]/[target_rounds]"

    # state machine: wait -> prompt -> evaluate
    if waiting:
        text "Pedal... pedal...":
            xalign 0.5
            yalign 0.45
        timer 0.1 repeat True action If(
            (renpy.get_time() - prompt_t) >= next_wait,
            true=[SetScreenVariable("waiting", False), SetScreenVariable("prompt_t", renpy.get_time())],
            false=NullAction()
        )
    else:
        text "DODGE!":
            xalign 0.5
            yalign 0.40

        # Big button for reaction
        button:
            xalign 0.5
            yalign 0.55
            xsize 320
            ysize 120
            text "CLICK"
            action Function(_mg_delivery_click, job_state, score, rounds, target_rounds, prompt_t, window)

        timer 0.05 repeat True action If(
            (renpy.get_time() - prompt_t) > window,
            true=Function(_mg_delivery_miss, job_state, score, rounds, target_rounds),
            false=NullAction()
        )

init -2 python:
    def _mg_delivery_click(job_state, score, rounds, target_rounds, prompt_t, window):
        # clicked in time
        if (renpy.get_time() - prompt_t) <= window:
            score += 1
        rounds += 1
        if score >= target_rounds:
            renpy.return_statement({"success": True, "score": score})
            return
        if rounds >= target_rounds + 2:
            renpy.return_statement({"success": False, "score": score})
            return
        # reset
        renpy.restart_interaction()
        # mutate screen vars via renpy.set_screen_variable
        renpy.set_screen_variable("score", score)
        renpy.set_screen_variable("rounds", rounds)
        renpy.set_screen_variable("waiting", True)
        renpy.set_screen_variable("prompt_t", renpy.get_time())
        renpy.set_screen_variable("next_wait", renpy.random.uniform(job_state["shift"].get("min_wait", 0.7), job_state["shift"].get("max_wait", 2.2)))

    def _mg_delivery_miss(job_state, score, rounds, target_rounds):
        rounds += 1
        if rounds >= target_rounds + 2:
            renpy.return_statement({"success": False, "score": score})
            return
        renpy.set_screen_variable("rounds", rounds)
        renpy.set_screen_variable("waiting", True)
        renpy.set_screen_variable("prompt_t", renpy.get_time())
        renpy.set_screen_variable("next_wait", renpy.random.uniform(job_state["shift"].get("min_wait", 0.7), job_state["shift"].get("max_wait", 2.2)))
        renpy.restart_interaction()


# -----------------------------
# Nursing Home: Care + Memory
# -----------------------------
screen mg_care_dialogue(job_state):
    default trust = job_state["shift"].get("start_trust", 2)
    default beat = 0

    $ shift = job_state["shift"]
    $ beats = shift.get("beats", [])
    $ title = shift.get("title", "Care Shift")

    tag minigame
    add shift.get("bg", Solid("#0f1012"))

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text title
        text "Trust: [trust]"

    if beat < len(beats):
        $ b = beats[beat]
        frame:
            xalign 0.5
            yalign 0.35
            padding (20, 16)
            vbox:
                spacing 10
                text b.get("line", "...")
                for opt in b.get("options", []):
                    textbutton opt["text"] action [
                        SetScreenVariable("trust", trust + opt.get("trust_delta", 0)),
                        SetScreenVariable("beat", beat + 1)
                    ]
    else:
        # require trust threshold or fall into memory match
        if trust >= shift.get("pass_trust", 3):
            text "They relax, just enough.":
                xalign 0.5
                yalign 0.55
            textbutton "Finish shift" xalign 0.5 yalign 0.65 action Return({"success": True, "trust": trust})
        else:
            text "You need to help them remember.":
                xalign 0.5
                yalign 0.52
            textbutton "Start Memory Match" xalign 0.5 yalign 0.62 action Return({"success": None, "trust": trust})


screen mg_memory_match(job_state):
    default revealed = []     # indices currently flipped (max 2)
    default matched = set()   # indices matched
    default moves = 0

    $ shift = job_state["shift"]
    $ pairs = shift.get("pairs", [("Rose", "Rose"), ("Key", "Key"), ("Photo", "Photo"), ("Map", "Map")])
    $ flat = []
    python:
        for a, b in pairs:
            flat.append(a)
            flat.append(b)
        renpy.random.shuffle(flat)
    $ target = len(flat)

    tag minigame
    add shift.get("bg", Solid("#0f1012"))

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text "Memory Match"
        text "Moves: [moves]  Matched: [len(matched)]/[target]"

    # grid
    grid 4 2:
        xalign 0.5
        yalign 0.55
        spacing 12
        for i in range(target):
            $ face = (i in revealed) or (i in matched)
            button:
                xsize 140
                ysize 70
                text (flat[i] if face else "?")
                action Function(_mg_flip_card, i)

    if len(matched) >= target:
        textbutton "Finish shift" xalign 0.5 yalign 0.90 action Return({"success": True, "moves": moves})

init -2 python:
    def _mg_flip_card(i):
        revealed = renpy.get_screen_variable("revealed")
        matched = renpy.get_screen_variable("matched")
        moves = renpy.get_screen_variable("moves")

        if i in matched:
            return

        if i in revealed:
            return

        revealed = list(revealed) + [i]
        renpy.set_screen_variable("revealed", revealed)

        if len(revealed) == 2:
            moves += 1
            renpy.set_screen_variable("moves", moves)
            # compare
            # We need access to shuffled list; easiest: store it in screen variable.
            # So we just force a short pause and then reset in label logic (handled in job_nursing.rpy).
        renpy.restart_interaction()


# -----------------------------
# Creative Contract: Poster Builder
# -----------------------------
screen mg_poster_builder(job_state):
    default chosen_bg = None
    default chosen_icon = None
    default placed = []   # list of {"part": str, "x": int, "y": int}
    default done = False

    $ shift = job_state["shift"]
    $ title = shift.get("title", "Creative Contract")
    $ req = shift.get("requirements", [])
    $ bgs = shift.get("poster_bgs", ["poster_bg_1", "poster_bg_2"])
    $ parts = shift.get("poster_parts", ["symbol", "moon", "truck", "handprint", "flower"])

    tag minigame
    add Solid("#0b0b0e")

    vbox:
        xalign 0.02
        yalign 0.02
        spacing 6
        text title
        $ req_text = "Requirements: " + ", ".join(req) if req else "Requirements: (none)"
        text req_text
        textbutton "Submit" action SetScreenVariable("done", True)

    # simple UI: select background, then click to place an icon
    frame:
        xalign 0.02
        yalign 0.18
        padding (12, 10)
        vbox:
            spacing 6
            text "Background"
            for bg in bgs:
                textbutton bg action SetScreenVariable("chosen_bg", bg)

            text "Icon"
            for p in parts:
                textbutton p action SetScreenVariable("chosen_icon", p)

    # poster canvas
    frame:
        xalign 0.58
        yalign 0.52
        xsize 600
        ysize 420
        padding (10, 10)

        add Solid("#1a1a22")

        if chosen_bg:
            text "[chosen_bg]" xalign 0.5 yalign 0.08

        for pl in placed:
            text "[pl['part']]" xpos pl["x"] ypos pl["y"]

        button:
            xfill True
            yfill True
            background None
            action Function(_mg_place_icon)

    if done:
        timer 0.1 action Return({"success": True, "placed": placed, "bg": chosen_bg, "icon": chosen_icon})

init -2 python:
    def _mg_place_icon():
        icon = renpy.get_screen_variable("chosen_icon")
        if not icon:
            return
        placed = list(renpy.get_screen_variable("placed"))
        # place near center with slight randomness
        x = int(renpy.random.uniform(80, 520))
        y = int(renpy.random.uniform(100, 320))
        placed.append({"part": icon, "x": x, "y": y})
        renpy.set_screen_variable("placed", placed)
        renpy.restart_interaction()
