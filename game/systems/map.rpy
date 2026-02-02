# systems/map.rpy
# Holds the world map screen and map navigation.
# This file is UI + jumps only. It does not contain story logic.

# ---------------------------------------------------------------------------
# Map Screen
# ---------------------------------------------------------------------------

# IMPORTANT NOTE:
# current_location does NOT mean "story location".
# It means "which interaction overlay should be active".

screen main_map():

    modal True
    zorder 50

    # Background
    add "images/scenes/main_map/main_map.png"

    # -----------------------------------------------------------------------
    # Map Buttons
    # -----------------------------------------------------------------------
    # NOTE:
    # Each hotspot uses existing images:
    #   images/scenes/main_map/<name>.png
    #   images/scenes/main_map/<name>_hover.png
    #
    # WILL need to tweak xpos/ypos to match map art.
    # Start rough, then nudge until it lines up.
    # -----------------------------------------------------------------------
    
    
    
    # -------------------------
    # Church
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/church.png"
        hover "images/scenes/main_map/church_hover.png"
        xpos 875
        ypos 0
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("church_exterior")
            ]

    # -------------------------
    # Gym
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/gym.png"
        hover "images/scenes/main_map/gym_hover.png"
        xpos 1225
        ypos 525
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("gym_exterior")
            ]

    # -------------------------
    # Home
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/home.png"
        hover "images/scenes/main_map/home_hover.png"
        xpos 0
        ypos 335
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("house_exterior")
            ]

    # -------------------------
    # Mall
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/mall.png"
        hover "images/scenes/main_map/mall_hover.png"
        xpos 1550
        ypos 675
        action [
            Hide("main_map"),
            SetVariable("current_location", None),
            Jump("mall_exterior")
            ]

    # -------------------------
    # University
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/university.png"
        hover "images/scenes/main_map/university_hover.png"
        xpos 450
        ypos 0
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("university_exterior")
            ]


    # -------------------------
    # PI Office
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/private_eye.png"
        hover "images/scenes/main_map/private_eye_hover.png"
        xpos 200
        ypos 15
        action [
            Hide("main_map"), 
            SetVariable("current_location", None), 
            Jump("pi_office_exterior")
            ]


    # -------------------------
    # Psychic
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/psychic.png"
        hover "images/scenes/main_map/psychic_hover.png"
        xpos 525
        ypos 550
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("psychic_exterior")
            ]



    # -------------------------
    # Warehouse
    # -------------------------
    imagebutton:
        idle "images/scenes/main_map/warehouse.png"
        hover "images/scenes/main_map/warehouse_hover.png"
        xpos 1600
        ypos 250
        action [
            Hide("main_map"),
            SetVariable("current_location", None), 
            Jump("warehouse_exterior")
            ]

    # -------------------------
    # Close map (stay where you are)
    # -------------------------
    textbutton "Close":
        xpos 30
        ypos 30
        action Hide("main_map")