### House.rpy #####


# The house is more detailed and will likely grow into
# a small internal navigation map later.


label house_hallway:
    scene bg house hallway:
        xysize (config.screen_width, config.screen_height)
    menu:
        "Kitchen":
            jump house_kitchen
        "Bathroom":
            jump house_bathroom
        "Bedroom":
            jump house_bedroom
        "Back to entry":
            jump house_entry

label house_kitchen:
    scene bg house kitchen:
        xysize (config.screen_width, config.screen_height)
    "The kitchen feels cold."
    menu:
        "Back to hallway":
            jump house_hallway

label house_bathroom:
    scene bg house bathroom:
        xysize (config.screen_width, config.screen_height)
    "The mirror makes you uneasy."
    menu:
        "Back to hallway":
            jump house_hallway

label house_bedroom:
    scene bg house bedroom:
        xysize (config.screen_width, config.screen_height)
    "Your room. It should feel safe."
    menu:
        "Back to hallway":
            jump house_hallway
