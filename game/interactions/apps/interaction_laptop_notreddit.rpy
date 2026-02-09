################################################################################
# interaction_laptop_notreddit.rpy
################################################################################

# ---------------------------------
# Variables
# ---------------------------------
default notreddit_mode = "home"

# Live text shown in the compose popup
default notreddit_title = ""
default notreddit_body  = ""

default notreddit_has_posted = False

default nr_title_clicked_once = False
default nr_body_clicked_once  = False


# ---------------------------------
# Auto-typing engine state
# ---------------------------------

default nr_auto_typing   = False
default nr_auto_title    = ""         # target title text
default nr_auto_body     = ""         # target body text
default nr_type_i_title  = 0
default nr_type_i_body   = 0

# ------------------------------------------------------------
# Functions that handle automatically typing the post text
# ------------------------------------------------------------

init python:
    def nr_start_typing(title_text, body_text):
        s = renpy.store
        
        if s.notreddit_has_posted:
            return

        if kind == "title":
            if s.nr.nr_title_clicked_once:
                return   

            s.nr_title_clicked_once = True     
            s.notreddit_title   = ""
            s.nr_auto_title     = title_text
            s.nr_type_i_title   = 0

        elif kind == "body":
            if s.nr.nr_title_clicked_once:
                return   

            s.nr_body_clicked_once = True 
            s.notreddit_body    = ""
            s.nr_auto_body      = body_text
            s.nr_type_i_body    = 0

        s.nr_auto_typing    = True

    def nr_tick_typing(step=1):
        s = renpy.store
        if not s.nr_auto_typing:
            return

        if s.nr_type_i_title < len(s.nr_auto_title):
            end = min(s.nr_type_i_title + step, len(s.nr_auto_title))
            s.notreddit_title += s.nr_auto_title[s.nr_type_i_title:end]
            s.nr_type_i_title = end

        elif s.nr_type_i_body < len(s.nr_auto_body):
            end = min(s.nr_type_i_body + step, len(s.nr_auto_body))
            s.notreddit_body += s.nr_auto_body[s.nr_type_i_body:end]
            s.nr_type_i_body = end

        else:
            s.nr_auto_typing = False

# ---------------------------------------------------------------------------
# Ghost Animation
# ---------------------------------------------------------------------------


    def nr_on_post_submitted():
        s = renpy.store

        s.notreddit_has_posted = True

        s.notreddit_post_title = s.notreddit_title
        s.notreddit_post_body = s.notreddit_body

        renpy.store.obj_complete("prog.onboarding.make_post")

        # Optional debug toast
        renpy.notify("Posted to NotReddit.")

        # IMPORTANT: do not call a label from here
        # Let your story loop detect the flag and continue.


    def nr_reset_typing():
        s = renpy.store

        s.nr_auto_typing = False
        s.nr_auto_title  = ""
        s.nr_auto_body   = ""
        s.nr_type_i_title = 0
        s.nr_type_i_body  = 0

    def nr_start_typing_field(kind, text_value):
        s = renpy.store

        if kind == "title":

            if s.nr_title_clicked_once:
                return
            
            s.nr_title_clicked_once = True

            s.notreddit_title = ""
            s.nr_auto_title   = text_value
            s.nr_type_i_title = 0

        elif kind == "body":
            if s.nr_body_clicked_once:
                return
            
            s.nr_body_clicked_once = True

            s.notreddit_body  = ""
            s.nr_auto_body    = text_value
            s.nr_type_i_body  = 0

        s.nr_auto_typing = True


# ---------------------------------
# NotReddit main screen
# ---------------------------------

screen laptop_notreddit_interactions():

    default nr_editing = None

    if notreddit_mode == "home":
        add "images/laptop/notreddit_home_screen.png"  align (0.5, 3.0) yoffset 50
        
        imagebutton:
            idle "images/laptop/notreddit_inaght_link.png"
            hover "images/laptop/notreddit_inaght_link_hover.png"
            xpos 1310 ypos 695
            action SetVariable("notreddit_mode", "inaght")

        textbutton "Close":
            xpos 1650 ypos 80
            action SetVariable("notreddit_mode", "home")
            
    elif notreddit_mode == "inaght":

        if notreddit_has_posted:
            add "images/laptop/notreddit_INAGHT_screen_afterpost.png" align (0.5, -6.0) yoffset 50
        else:    
            add "images/laptop/notreddit_INAGHT_screen.png"  align (0.5, -6.0) yoffset 50        

        # Create Post → opens popup (no page switch)
        imagebutton:
            idle  "images/laptop/notreddit_create_post.png"
            hover "images/laptop/notreddit_create_post_hover.png"
            xpos 1200
            ypos 415
            sensitive (not notreddit_has_posted)
            action Show("notreddit_compose_popup")

        textbutton "Close":
            xpos 1650 ypos 80
            action SetVariable("notreddit_mode", "home")

    elif notreddit_mode == "posted":
        # This is the "new reddit page" you want to show after posting
        add "images/laptop/notreddit_INAGHT_screen_afterpost.png" align (0.5, 0.8) yoffset 50


# ------------------------------
# Compose popup (modal)
# ------------------------------

screen notreddit_compose_popup():

    modal True
    zorder 100

    # Compose UI (center/offset as needed)
    add "images/laptop/notreddit_post_screen.png" xpos 500 ypos 200

        # Close/X
    textbutton "X":
        xpos 1500
        ypos 120
        action [ Hide("notreddit_compose_popup"), Function(nr_reset_typing) ]


    # Title image — clicking starts auto-typing the Subject
    imagebutton:
        idle  "images/laptop/notreddit_post_title.png"
        hover "images/laptop/notreddit_post_title_hover.png"
        xpos 510
        ypos 325
        action Function(nr_start_typing_field, "title",
                        "Starting a ghost-hunting team")

    # Body image — clicking starts auto-typing the Body
    imagebutton:
        idle  "images/laptop/notreddit_post_body.png"
        hover "images/laptop/notreddit_post_body_hover.png"
        xpos 525
        ypos 550
        action Function(nr_start_typing_field, "body",
                        "I live in a one-bedroom apartment, I’m broke, and I have no gear.\n"
                        "So obviously I decided to start a paranormal investigation group.\n"
                        "\n"
                        "Requirements:\n"
                        "• alive (preferably)\n"
                        "• okay with the fact that we will look clueless\n")
    # Live title text overlay
    frame:
        xpos 525
        ypos 350
        xsize 980
        ysize 60
        background None
        text notreddit_title:
            size 28
            color "#FFFFFF"
            outlines []

    # Live body text overlay
    frame:
        xpos 550
        ypos 595
        xsize 980
        ysize 360
        background None
        text notreddit_body:
            size 26
            color "#FFFFFF"
            outlines []
            layout "subtitle"


    # Post button
    imagebutton:
        idle  "images/laptop/notreddit_post_button.png"
        hover "images/laptop/notreddit_post_button_hover.png"
        xpos 1355
        ypos 830
        action If(
    (notreddit_title.strip() != "") and (notreddit_body.strip() != "") and (not nr_auto_typing),
            [
            # Save what was typed as the actual posted content
            SetVariable("notreddit_post_title", notreddit_title),
            SetVariable("notreddit_post_body", notreddit_body),

            # Switch the NotReddit screen to the "posted" version
            SetVariable("notreddit_mode", "posted"),

            # Close the compose popup and clear the typing state
            Hide("notreddit_compose_popup"),
            Function(nr_reset_typing),

            # Fire story logic (objective complete + dialogue label)
            Function(nr_on_post_submitted)
            ],
            Notify("Finish writing the post first.")
        )

    # Auto-typing driver
    if nr_auto_typing:
        timer 0.03 action Function(nr_tick_typing, 1) repeat True      

        