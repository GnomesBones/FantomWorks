# interaction_hub.rpy

################################################################################
# One screen to rule them all. Do not show room screens directly.
################################################################################


# Location keys (helps prevent typos later)
define LOC_BEDROOM  = "bedroom"
define LOC_KITCHEN  = "kitchen"
define LOC_BATHROOM = "bathroom"
define LOC_HALLWAY  = "hallway"
define LOC_ENTRY    = "entry"

# Where the player is right now
#default current_location = LOC_BEDROOM

# Optional: a simple helper so labels can call one thing
init python:
    def set_location(loc):
        renpy.store.current_location = loc

screen interaction_hub():

    # If you ever want to temporarily disable interactions, set current_location = None
    if current_location is None:
        pass

    elif current_location == LOC_BEDROOM:
        use interaction_bedroom

    # Add these when you create the screens:
    # elif current_location == LOC_KITCHEN:
    #     use interaction_kitchen
    # elif current_location == LOC_BATHROOM:
    #     use interaction_bathroom
    # elif current_location == LOC_HALLWAY:
    #     use interaction_hallway
    # elif current_location == LOC_ENTRY:
    #     use interaction_entry

    else:
        # Fallback so you instantly notice missing wiring
        frame:
            xalign 0.5
            yalign 0.05
            padding (18, 10)
            text "No interaction screen for: [current_location]"
