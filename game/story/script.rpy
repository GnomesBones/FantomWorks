# game/story/script.rpy

# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------

# Track objective changes and completions (NOT defined elsewhere in your project)
default _last_pinned_step_id = None
default _last_objective_history_len = 0


# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

# Player character (with dynamic name)
define player = Character("[player_name]", dynamic=True)

# ---------------------------------------------------------------------------
# The game starts here.
# ---------------------------------------------------------------------------
label start_story:

    $ current_location = LOC_BEDROOM
    
    # Exists in: game/systems/time_and_events.rpy
    call time_system_begin

    # Exists in: game/systems/objectives.rpy
    call objectives_begin


    scene bg bedroom with fade:
        zoom 1.0
        xalign 0.5
        yalign 0.5

    call objectives_begin

    $ player_sprite = f"{player_gender}_{player_race}_{player_outfit}_{player_body}_{player_emotion}"
    show expression player_sprite as player:
        xalign 0.5
        yalign 1.0

    player "It's late..."

    window hide
    hide player
    with dissolve

 
    player "I want to make a ghost hunting team, maybe a post on notreddit."
    window hide

    show screen interaction_bedroom

    $ add_status("hexed")
    $ add_status("stressed")
    $ lose_sanity(75)
    $ remove_status("stressed")

    # Initialize trackers so we do not spam dialogue on first frame
    $ _last_pinned_step_id = pinned_step_id
    $ _last_objective_history_len = len(objective_history)

    jump hub_loop

# ---------------------------------------------------------------------------
# Hub loop: keeps game alive, reacts to objective progression with dialogue
# ---------------------------------------------------------------------------


label hub_loop:

    # Flavor lines keyed to the FULL step id (quest.step)
    $ _pin_flavor = {
        "prog.onboarding.sleep_1": "Sleep. Let the internet do its thing.",
        "prog.onboarding.wait_replies_1": "Objective pinned: Wait for replies. The thread is a slow creature.",
        "prog.onboarding.check_inneed": "Objective pinned: Check InNeed. Work shows up when you look for it.",
        "prog.onboarding.free_reign_house": "Objective pinned: Free time. The house feels bigger when you have options.",
        "prog.onboarding.read_replies_mandatory": "Objective pinned: Read replies. You can’t ignore it forever.",
        "prog.onboarding.set_meetup": "Objective pinned: Set the meet up. This is the point of no take-backs.",
        "prog.onboarding.sleep_2": "Objective pinned: Sleep. Tomorrow has teeth.",
        "prog.onboarding.read_replies_mandatory_2": "Objective pinned: Read replies. New messages. New pressure.",
        "prog.onboarding.meet_team": "Objective pinned: Meet the team. Leave the house and make it real.",
    }

    while True:

        # 1) If pinned objective changed, say a line once
        if pinned_step_id != _last_pinned_step_id and pinned_step_id is not None:

            $ line = _pin_flavor.get(pinned_step_id, None)
            if line:
                narrator "[line]"

            $ _last_pinned_step_id = pinned_step_id


        # 2) If an objective completed, objective_history grows. React once per new entry.
        if len(objective_history) > _last_objective_history_len:

            $ newest = objective_history[-1]
            $ _last_objective_history_len = len(objective_history)


        # 3) Keep the hub running
        # The actual progression is driven by your screens calling obj_complete(...)
        pause 0.15

        show screen interaction_bedroom