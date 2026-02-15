# game/ui/pause_menu.rpy

# ---------------------------------------------------------------------------
# Helper: pick the best available sprite file for the pause menu
# ---------------------------------------------------------------------------
init python:
    def player_sprite_path():
        """
        Returns a file path for the player's sprite based on:
        gender, race, outfit, body, emotion.

        Tries emotion-specific first, then a base fallback, then missing sprite.
        """
        emo_name  = f"{player_gender}_{player_race}_{player_outfit}_{player_body}_{player_emotion}.png"
        base_name = f"{player_gender}_{player_race}_{player_outfit}_{player_body}.png"

        # Change this folder if your pause sprites live elsewhere.
        folder = "images/character_creation/emotions/"

        emo_path  = folder + emo_name
        base_path = folder + base_name

        if renpy.loadable(emo_path):
            return emo_path
        if renpy.loadable(base_path):
            return base_path

        renpy.log(f"Missing pause sprite: tried {emo_path} and {base_path}")
        return "gui/missing.png"


# ---------------------------------------------------------------------------
# Pause Menu Screen
# ---------------------------------------------------------------------------
screen pause():
    tag menu
    modal True
    zorder 100

    fixed:
        xfill True
        yfill True

        add Solid("#000000CC")

        add "gui/pause_frame.png":
            xalign 0.5
            yalign 0.5

        # Player sprite (file path returned by player_sprite_path)
        add DynamicImage(player_sprite_path()):
            xalign 0.5
            yalign 0.55

        # Left column
        textbutton "Inventory":
            action ShowMenu("inventory")
            style "pause_bt"
            xalign 0.20
            yalign 0.15

        textbutton "Evidence Gathered":
            action ShowMenu("evidence")
            style "pause_bt"
            xalign 0.20
            yalign 0.45

        textbutton "Options":
            action ShowMenu("preferences")
            style "pause_bt"
            xalign 0.20
            yalign 0.75

        # Right column
        textbutton "Objective":
            action ShowMenu("objective")
            style "pause_bt"
            xalign 0.80
            yalign 0.15

        textbutton "Case Files":
            action ShowMenu("case_files")
            style "pause_bt"
            xalign 0.80
            yalign 0.45

        textbutton "Relationships":
            action ShowMenu("relationships")
            style "pause_bt"
            xalign 0.80
            yalign 0.75

    # Close pause with common keys
    key "toggle_pause" action Return()
    key "game_menu" action Return()
    key "K_ESCAPE" action Return()
