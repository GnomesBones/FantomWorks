# script.rpy

# The script of the game goes in this file.

##Variables##

default hud_visible = True

# Declare characters used by this game. The color argument colorizes the
# name of the character.

# Player character (with dynamic name)
define player = Character("[player_name]", dynamic=True)


# The game starts here.

label start_story:

    $ current_location = LOC_BEDROOM
    call time_system_begin
    call objectives_begin


    scene bg bedroom with fade:
        zoom 1.0
        xalign 0.5
        yalign 0.5

    call objectives_begin

    $ player_sprite = f"{player_gender}_{player_race}_{player_outfit}_{player_body}_{player_emotion}"
    show expression player_sprite as player:
        xalign 0.5
        yalign 1.0

    player "It's late..."

    window hide
    hide player
    with dissolve

 
    player "I want to make a ghost hunting team, maybe a post on notreddit."
    window hide

    show screen interaction_bedroom

    $ add_status("hexed")
    $ add_status("stressed")
    $ lose_sanity(75)
    $ remove_status("stressed")

    pause

    return
