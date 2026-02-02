# core/game_state.rpy

# Where the player is standing (drives interaction_hub)
#default current_location = "bedroom"

# Main story step
default current_objective = "post_notreddit"

# Flags (use these to gate buttons and scenes)
default obj_post_notreddit_done = False
default obj_meet_team_done = False
default obj_first_mission_ready = False

# Text shown in HUD/pause menu later if you want it
define OBJECTIVE_TEXT = {
    "post_notreddit": "Make a NotReddit post to recruit a team.",
    "meet_team": "Meet the people who replied.",
    "prep_mission": "Get ready for the first mission.",
    "choose_team": "Choose who is going with you.",
    "go_bobby": "Head to Billy Marlowe's Dance Barn.",
    "gather_evidence": "Gather evidence inside.",
    "process_evidence": "Go home and log your findings.",
}

init python:
    def set_objective(name):
        store.current_objective = name

    def objective_text():
        return OBJECTIVE_TEXT.get(store.current_objective, "")

    def complete_objective(name):
        # tiny helper, optional
        if name == "post_notreddit":
            store.obj_post_notreddit_done = True
        elif name == "meet_team":
            store.obj_meet_team_done = True
        elif name == "prep_mission":
            store.obj_first_mission_ready = True
