init python:
    def player_logo():
        return f"images/character_creation/icons/{player_gender}_{player_race}_{player_outfit}_{player_emotion}_{player_body}_logo.png"


screen hud_display():
    modal False

    fixed:
        add "images/hud/equipment_border.png" xpos 1650 ypos 0.70
        add "images/hud/player_status_border.png" xpos 300 ypos 0.70 

        add player_logo() size (285, 310) xpos 40 ypos 0.70

        add "images/hud/icon_border.png" xpos 20 ypos 0.70    

 
