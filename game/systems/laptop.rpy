################################################################################
# laptop.rpy
################################################################################
# Shell frame
image laptop_shell      = "assets/images/laptop/laptop_shell.png"

# Desktop / home background
image laptop_home       = "assets/images/laptop/laptop_screen.png"

# ---------------------------
# State
# ---------------------------
default laptop_page = "home"

# ---------------------------
# Main laptop screen
# ---------------------------
screen laptop():
    modal True
    
    #Dim Background
    add Solid((0, 0, 0, 128))

    # Draw current page
    add "laptop_home" align (0.5, 0.34) yoffset 50

    # Route to page-specific interaction layer
    if laptop_page == "home":
        use laptop_home_interactions
    elif laptop_page == "inneed":
        pass
    elif laptop_page == "notreddit":
        use laptop_notreddit_interactions
    elif laptop_page == "schedule":
        pass
    elif laptop_page == "utoob":
        pass
    elif laptop_page == "webdive":
        pass

    # Draw the shell on top
    add "laptop_shell" align (0.5, 0.5) yoffset 50

    # Close controls
    textbutton "Close":
        xpos 1650 ypos 80
        action Hide("laptop")

    key "game_menu" action Hide("laptop")   # ESC
    key "mouseup_3" action Hide("laptop")   # Right click

# ---------------------------
# Home interactions (icons -> other files' screens)
# Keep this one here per your request.
# ---------------------------
screen laptop_home_interactions():

    # Example icon hitboxes. Replace xpos/ypos with your real positions.
    # These use the *_icon.png / *_icon_hover.png files you listed.
    imagebutton:
        idle "assets/images/laptop/inneed_icon.png"
        hover "assets/images/laptop/inneed_icon_hover.png"
        xpos 354 ypos 200
        action SetVariable("laptop_page", "inneed")

    imagebutton:
        idle "assets/images/laptop/notreddit_icon.png"
        hover "assets/images/laptop/notreddit_icon_hover.png"
        xpos 355 ypos 351
        action SetVariable("laptop_page", "notreddit")

    imagebutton:
        idle "assets/images/laptop/schedule_icon.png"
        hover "assets/images/laptop/schedule_icon_hover.png"
        xpos 355 ypos 665
        action SetVariable("laptop_page", "schedule")

    imagebutton:
        idle "assets/images/laptop/utoob_icon.png"
        hover "assets/images/laptop/utoob_icon_hover.png"
        xpos 505 ypos 265
        action SetVariable("laptop_page", "utoob")

    imagebutton:
        idle "assets/images/laptop/webdive_icon.png"
        hover "assets/images/laptop/webdive_icon_hover.png"
        xpos 670 ypos 578
        action SetVariable("laptop_page", "webdive")

    imagebutton:
        idle "assets/images/laptop/photos_icon.png"
        hover "assets/images/laptop/photos_icon_hover.png"
        xpos 665 ypos 420
        action SetVariable("laptop_page", "photos")

