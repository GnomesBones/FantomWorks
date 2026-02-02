# interaction_bedroom.rpy

################################################################################
## Standard interaction
################################################################################

screen interaction_bedroom():
    imagebutton:
        xpos 1475 ypos 755    
        idle "images/scenes/house/bedroom_backpack.png"
        hover "images/scenes/house/bedroom_backpack_hover.png"
        action Show("inventory")

    imagebutton:
        xpos 875 ypos 35    
        idle "images/scenes/house/bedroom_board.png"
        hover "images/scenes/house/bedroom_board_hover.png"
        action NullAction()

    imagebutton:
        xpos 1085 ypos 450    
        idle "images/scenes/house/bedroom_laptop.png"
        hover "images/scenes/house/bedroom_laptop_hover.png"
        action [Show("laptop"), SetVariable("current_location", None)]   

    imagebutton:
        xpos 1710 ypos 40    
        idle "images/scenes/house/bedroom_door.png"
        hover "images/scenes/house/bedroom_door_hover.png"
        action NullAction()        


## for all feminine characters

    if player_pronouns == "she":
        imagebutton:
            xpos 20 ypos 520
            idle "images/scenes/house/feminine_bedroom_bed.png"
            hover "images/scenes/house/feminine_bedroom_bed_hover.png"
            action NullAction()

        imagebutton:
            xpos 1275 ypos 620
            idle  "images/scenes/house/feminine_bedroom_phone.png"
            hover "images/scenes/house/feminine_bedroom_phone_hover.png"
            action NullAction()



#for all masculine characters

    elif player_pronouns == "he":
        imagebutton:
            xpos 5 ypos 550
            idle "images/scenes/house/bedroom_bed.png"
            hover "images/scenes/house/bedroom_bed_hover.png"
            action NullAction()
    
        imagebutton:
            xpos 527 ypos 700
            idle  "images/scenes/house/bedroom_phone.png"
            hover "images/scenes/house/bedroom_phone_hover.png"
            action NullAction()



# for all neutral characters

    else:

        imagebutton:

            xpos 5 ypos 550
            idle "images/scenes/house/bedroom_bed.png"
            hover "images/scenes/house/bedroom_bed_hover.png"
            action NullAction()

        imagebutton:

            xpos 527 ypos 700          
            idle  "images/scenes/house/bedroom_phone.png"
            hover "images/scenes/house/bedroom_phone_hover.png"
            action NullAction()
        


