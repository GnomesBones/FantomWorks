# game/ui/objectives_overlay.rpy

# ---------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------


default hide_objectives_overlay = False


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
    if not hide_objectives_overlay and not any([
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
                vbox:
                    spacing 8

                    text "Objective: [obj_current_text()]":
                        xalign 1.0
                        textalign 1.0
                        size 24
                        color "#FFFFFF"
                        outlines [(2, "#000000AA")]

                    $ buckets = obj_list_other_active_quests(max_per_type=2)

                    if buckets.get("job_quest"):
                        text "Jobs:":
                            xalign 1.0
                            textalign 1.0
                            size 18
                            color "#FFFFFF"
                            outlines [(2, "#000000AA")]

                        for title, nxt in buckets["job_quest"]:
                            text "• [title]: [nxt]":
                                xalign 1.0
                                textalign 1.0
                                size 16
                                color "#FFFFFF"
                                outlines [(2, "#000000AA")]

                    if buckets.get("investigative"):
                        text "Investigations:":
                            xalign 1.0
                            textalign 1.0
                            size 18
                            color "#FFFFFF"
                            outlines [(2, "#000000AA")]

                        for title, nxt in buckets["investigative"]:
                            text "• [title]: [nxt]":
                                xalign 1.0
                                textalign 1.0
                                size 16
                                color "#FFFFFF"
                                outlines [(2, "#000000AA")]

                    if buckets.get("character_arc"):
                        text "People:":
                            xalign 1.0
                            textalign 1.0
                            size 18
                            color "#FFFFFF"
                            outlines [(2, "#000000AA")]

                        for title, nxt in buckets["character_arc"]:
                            text "• [title]: [nxt]":
                                xalign 1.0
                                textalign 1.0
                                size 16
                                color "#FFFFFF"
                                outlines [(2, "#000000AA")]

                    if buckets.get("ghost_arc"):
                        text "Hauntings:":
                            xalign 1.0
                            textalign 1.0
                            size 18
                            color "#FFFFFF"
                            outlines [(2, "#000000AA")]

                        for title, nxt in buckets["ghost_arc"]:
                            text "• [title]: [nxt]":
                                xalign 1.0
                                textalign 1.0
                                size 16
                                color "#FFFFFF"
                                outlines [(2, "#000000AA")]

                    if buckets.get("player_progression"):
                        text "Progress:":
                            xalign 1.0
                            textalign 1.0
                            size 18
                            color "#FFFFFF"
                            outlines [(2, "#000000AA")]

                        for title, nxt in buckets["player_progression"]:
                            text "• [title]: [nxt]":
                                xalign 1.0
                                textalign 1.0
                                size 16
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