# character_creation.rpy

##Variables##

default equipment_list = []  # Start empty
default equipment_index = 0
default nerves = 100
default status_affect = "None"
default interference = "None"



default player_name = "Sam"
default player_pronouns = "they"
image bg bathroom = "menu/character_creation_bg.png"
default player_body = "soft"
default player_gender = "feminine"
default player_race     = "black"
default player_emotion = "idle"
default player_outfit = "casual"

default race_list = ["black", "latino", "asian", "white"]
default gender_list = ["feminine", "masculine"]

default race_index = 0
default gender_index = 0

## Character Creation ##

screen choose_character():

    tag menu
    modal True

    fixed:
             
        ## 1) Body Type ##
        text "How would you like to look?" xalign 0.50 yalign 0.025 style "heading_text"

        # Gender ⟨ Masculine ⟩ centered over the first sprite
        textbutton "<" xalign 0.27 yalign 0.095 action SetVariable(
            "gender_index", (gender_index - 1) % len(gender_list))
        text "[gender_list[gender_index].capitalize()]" xalign 0.35 yalign 0.095 style "selector_text"
        textbutton ">" xalign 0.43 yalign 0.095 action SetVariable(
            "gender_index", (gender_index + 1) % len(gender_list))

        # Race ⟨ White ⟩ centered over the last sprite
        textbutton "<" xalign 0.57 yalign 0.095 action SetVariable(
            "race_index",   (race_index   - 1) % len(race_list))
        text "[race_list[race_index].capitalize()]" xalign 0.65 yalign 0.095 style "selector_text"
        textbutton ">" xalign 0.73 yalign 0.095 action SetVariable(
            "race_index",   (race_index   + 1) % len(race_list))

        # Sync our vars
        $ player_gender = gender_list[gender_index]
        $ player_race   = race_list[race_index]

        # The three body-type buttons
        $ fn_slim    = "assets/images/character_creation/%s_slim_%s.png"    % (player_gender, player_race)
        $ fn_athletic= "assets/images/character_creation/%s_athletic_%s.png"% (player_gender, player_race)
        $ fn_soft    = "assets/images/character_creation/%s_soft_%s.png"    % (player_gender, player_race)

        # Slim
        if player_body == "slim":
            imagebutton:
                idle  Transform(DynamicImage(fn_slim), xysize=(345,685))
                hover Transform(DynamicImage(fn_slim), xysize=(345,685))
                at selected_highlight
                action SetVariable("player_body","slim")
                xalign 0.10 yalign 0.55
        else:
            imagebutton:
                idle  Transform(DynamicImage(fn_slim), xysize=(345,685))
                hover Transform(DynamicImage(fn_slim), xysize=(345,685))
                action SetVariable("player_body","slim")
                xalign 0.10 yalign 0.55

        # Athletic
        if player_body == "athletic":
            imagebutton:
                idle  Transform(DynamicImage(fn_athletic), xysize=(345, 685))
                hover Transform(DynamicImage(fn_athletic), xysize=(345, 685))
                at selected_highlight
                action SetVariable("player_body","athletic")
                xalign 0.50 yalign 0.55
        else:
            imagebutton:
                idle  Transform(DynamicImage(fn_athletic), xysize=(345,685))
                hover Transform(DynamicImage(fn_athletic), xysize=(345,685))
                action SetVariable("player_body","athletic")
                xalign 0.50 yalign 0.55

        # Soft
        if player_body == "soft":
            imagebutton:
                idle  Transform(DynamicImage(fn_soft), xysize=(345,685))
                hover Transform(DynamicImage(fn_soft), xysize=(345,685))
                at selected_highlight
                action SetVariable("player_body","soft")
                xalign 0.85 yalign 0.55
        else:
            imagebutton:
                idle  Transform(DynamicImage(fn_soft), xysize=(345,685))
                hover Transform(DynamicImage(fn_soft), xysize=(345,685))
                action SetVariable("player_body","soft")
                xalign 0.85 yalign 0.55

        ## Transparent Rectangle ##

        add Solid("#000000F2") xalign 0.5 yalign 1.0 xsize 1920 ysize 300

        ## 2) Name and Pronouns ##
        # Header
        text "What would you like to be called?" xalign 0.1 yalign 0.8 style "heading_text"

        # Name
        text "Typer here:" xalign 0.15 yalign 0.90
        input value VariableInputValue("player_name") xalign 0.25 yalign 0.90 xsize 350 ysize 80

        # Pronouns

        text "How would you like to be addressed?" xalign 1.0 yalign 0.8 style "heading_text"

        if player_pronouns == "he":
            textbutton "He/Him"    at selected_highlight action SetVariable("player_pronouns","he")    xalign 0.62 yalign 0.85
        else:
            textbutton "He/Him"    action SetVariable("player_pronouns","he")    xalign 0.62 yalign 0.85

        if player_pronouns == "she":
            textbutton "She/Her"   at selected_highlight action SetVariable("player_pronouns","she")   xalign 0.72 yalign 0.85
        else:
            textbutton "She/Her"   action SetVariable("player_pronouns","she")   xalign 0.72 yalign 0.85

        if player_pronouns == "they":
            textbutton "They/Them" at selected_highlight action SetVariable("player_pronouns","they") xalign 0.62 yalign 0.95
        else:
            textbutton "They/Them" action SetVariable("player_pronouns","they") xalign 0.62 yalign 0.95


        ## 3) Confirm ##
        textbutton "Confirm":
            xalign 0.98 yalign 0.98
            action [
                SetVariable("player_gender", gender_list[gender_index]),
                SetVariable("player_race", race_list[race_index]),
                Return()
            ]


## Begin code ##

label character_creation:
    
    scene bg bathroom with fade:
        zoom 1.5
        xalign 0.5
        yalign 0.5

    "Before we begin, tell us about yourself..."

    call screen choose_character



    "Good Luck, [player_name]..."

    jump start_story
