# pause_menu.rpy

init -3 python:
    def player_sprite():
        # match your on-disk naming, five fields:
        emo_name  = f"{player_gender}_{player_race}_{player_outfit}_{player_body}_{player_emotion}.png"
        base_name = f"{player_gender}_{player_race}_{player_outfit}_{player_body}.png"

        emo_path  = "images/character_creation/emotions/" + emo_name
        base_path = "images/character_creation/emotions/" + base_name

        if renpy.loadable(emo_path):
            return emo_path
        elif renpy.loadable(base_path):
            return base_path
        else:
            # fallback to a known “missing” sprite so you don’t crash
            renpy.log(f"Missing sprite: tried {emo_path} and {base_path}")
            return "gui/missing.png"

screen pause():
    tag menu
    modal True
    zorder 100

    fixed:
        add Solid("#000000CC")

        add "gui/pause_frame.png" xalign 0.5 yalign 0.5

        # call the function (the () is mandatory):
        add DynamicImage(player_sprite()) xalign 0.5 yalign 0.55

        textbutton "Inventory"        action ShowMenu("inventory")    style "pause_bt" xalign 0.20 yalign 0.15
        textbutton "Evidence Gathered" action ShowMenu("evidence")     style "pause_bt" xalign 0.20 yalign 0.45
        textbutton "Options"          action ShowMenu("preferences")  style "pause_bt" xalign 0.20 yalign 0.75

        textbutton "Objective"        action ShowMenu("objective")    style "pause_bt" xalign 0.80 yalign 0.15
        textbutton "Case Files"       action ShowMenu("case_files")   style "pause_bt" xalign 0.80 yalign 0.45
        textbutton "Relationships"    action ShowMenu("relationships") style "pause_bt" xalign 0.80 yalign 0.75

    key "toggle_pause" action Hide("pause")
    key "game_menu"    action Hide("pause")
