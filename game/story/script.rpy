# script.rpy

################################################################################
## The script of the game goes in this file.
################################################################################



##Variables##

default hud_visible = True


image bg bedroom = ConditionSwitch(
    "player_pronouns == 'she'", "assets/images/scenes/house/feminine_bedroom_bg.png",
    "player_pronouns == 'he'", "assets/images/scenes/house/masculine_bedroom_bg.png",
    "True", "assets/images/scenes/house/bedroom_bg.png"  # Fallback
)

# Declare characters used by this game. The color argument colorizes the
# name of the character.

# Player character (with dynamic name)
define player = Character("[player_name]", dynamic=True)


# The game starts here.

label start_story:
    
 
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg bedroom with fade:
        zoom 1.0
        xalign 0.5
        yalign 0.5


    # This shows a character sprite. 

    # Use this format to show your player with all attributes

    show player:
        # This will look for: gender_race_outfit_body_emotion.png
        "[player_gender]_[player_race]_[player_outfit]_[player_body]_[player_emotion]"
        # Example result: "feminine_black_casual_soft_happy.png"
        xalign 0.5 
        yalign 1.0 # Position as needed

    # These display lines of dialogue.

    player "It's late..."
#    player "Not 'staying up' late."
#    player "More like why am I still awake doom scrolling?"

    window hide
    hide player 
    with dissolve
    # This shows a screens. 

    player "I want to make a ghost hunting team, maybe a post on notreddit."
    window hide
    
    show screen interaction_bedroom

    show screen hud_display
    $ add_status("hexed")
    $ add_status("stressed")
    $ lose_sanity(75)



    pause

    $ remove_status("stressed")

    player "Beta Done"

    return
