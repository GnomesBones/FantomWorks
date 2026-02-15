# game/ui/objectives_overlay.rpy

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

init -2 python:
    if "objectives_overlay" not in config.overlay_screens:
        config.overlay_screens.append("objectives_overlay")

# ---------------------------------------------------------------------------
# Objective Overlay 
# ---------------------------------------------------------------------------

screen objectives_overlay():
    modal False
    zorder 95   # above HUD (10), below menu screens like journal_ui (100)

    # Hide during character creation so the UI is clean.
    if not any([
        renpy.get_screen("menu"),
        renpy.get_screen("choose_character"),
        renpy.get_screen("pause_menu"),
    ]):


        fixed:
            xfill True
            yfill True
        
            # Anchor the whole block to the top-right corner
            frame:
                xalign 1.0
                yalign 0.0
                xoffset -20
                yoffset 24

            # Background frame
                background "#00000055"
                padding (14, 10)
                xmaximum 520

                # Right-aligned label + wrapped objective text
                text "Objective: [obj_current_text()]":
                    xalign 1.0
                    textalign 1.0
                    size 24
                    color "#FFFFFF"
                    outlines [(2, "#000000AA")]

# ---------------------------------------------------------------------------
# Ghost Animation
# ---------------------------------------------------------------------------

image ghost_chase:
    "images/hud/HUD_ghost.png"

transform ghost_swoop:
    xalign -0.2
    yalign 0.05
    alpha 1.0
    linear 1.2 xalign 1.2 alpha 0.0

# ---------------------------------------------------------------------------
# Objective Complete FX
# ---------------------------------------------------------------------------

transform objective_chase_right:
    alpha 1.0
    yoffset 0
    linear 1.2 alpha 0.0 yoffset 10

screen objective_complete_fx(text_to_chase):
    zorder 200
    modal False

    fixed:
        xfill True
        yfill True

            # Anchor the whole block to the top-right corner
        frame:
            xalign 1.0
            yalign 0.0
            xoffset -20
            yoffset 24


            background "#00000055"
            padding (14, 10)
            xmaximum 520

            text text_to_chase:
                xalign 1.0
                textalign 1.0
                size 24
                color "#FFFFFF"
                outlines [(2, "#000000AA")]
                at objective_chase_right

    add "ghost_chase" at ghost_swoop

    timer 1.3 action Hide("objective_complete_fx")


label objective_complete_fx_show(text_to_show=""):
    show screen objective_complete_fx(text_to_chase=text_to_show)
    $ renpy.pause(1.2, hard=True)
    hide screen objective_complete_fx
    return