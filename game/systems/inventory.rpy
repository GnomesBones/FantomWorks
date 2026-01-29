## Inventory.rpy

# Player starts with nothing
default inventory = {}        # { item_id: count }

# Where each item’s small icon lives (use forward slashes)
define INVENTORY_ICONS = {
    "holy_water":        "images/inventory/equipment_slot_holy_water_small.png",
    "emf_reader":        "images/inventory/equipment_slot_emf_reader_small.png",
    "anomaly_detector":  "images/inventory/equipment_slot_anamoly_detector_small.png",
    "digital_recorder":  "images/inventory/equipment_slot_digital_recorder_small.png",
    "digital_camera":    "images/inventory/equipment_slot_digital_camera_small.png",
    "spirit_box":        "images/inventory/equipment_slot_spirit_box_small.png",
    "laser_therm":       "images/inventory/equipment_slot_laser_themometer_small.png",
    "mag_light":         "images/inventory/equipment_slot_mag_light_small.png",
    "obvilus":           "images/inventory/equipment_slot_obvilus_small.png",
    "rem_pod":           "images/inventory/equipment_slot_rem_pod_small.png",
    "go_pro":            "images/inventory/equipment_slot_go_pro_small.png",
    "bible":             "images/inventory/equipment_slot_bible_icon_small.png",
    # …add others as needed
}

# Fixed slot positions (edit these to “move” where icons land)
# These coords assume your backpack png fills the screen. Tweak to taste.
define INV_SLOTS = [
    (740, 290), (840, 290), (940, 290), (1040, 290),
    (740, 390), (840, 390), (940, 390), (1040, 390),
    (740, 490), (840, 490), (940, 490), (1040, 490),
]

# Helpers to mutate inventory
init python:
    def add_item(item_id, count=1):
        inventory[item_id] = inventory.get(item_id, 0) + count

    def remove_item(item_id, count=1):
        if item_id in inventory:
            inventory[item_id] -= count
            if inventory[item_id] <= 0:
                del inventory[item_id]

    def inventory_flat_list():
        """
        Expands {id: count} -> ['id','id', ...] so we can place one icon per slot.
        Holy water 4x becomes 4 entries, etc.
        """
        out = []
        for k, c in inventory.items():
            out.extend([k] * max(0, int(c)))
        return out
screen inventory():
    modal True

    fixed:
        add "images/inventory/backpack_inventory.png"

        # If empty, show your “nothing” message
        if not inventory:
            vbox:
                xalign 0.5
                yalign 0.4
                spacing 10

                text "Nothing":
                    color "#FFFFFF"
                    size 28
                    text_align 0.5
                    xalign 0.5

                frame:
                    xsize 400
                    ysize 2
                    background Solid("#FFFFFF")
                    xalign 0.5

                text "What do you expect? You just started the game.":
                    color "#FFFFFF"
                    size 28
                    text_align 0.5
                    xalign 0.5

        # Render item icons in fixed slots
        $ flat = inventory_flat_list()
        for i, (sx, sy) in enumerate(INV_SLOTS):
            if i < len(flat):
                $ item_id = flat[i]
                # draw the icon
                add INVENTORY_ICONS.get(item_id, "images/inventory/equipment_slot_mag_light_small.png"):
                    xpos sx
                    ypos sy
                    # optional scale
                    zoom 1.0

                # small count bubble for stacked items (show only on first of the stack)
                if inventory[item_id] > 1:
                    # count label near the bottom-right of the slot
                    text ("x" + str(inventory[item_id])):
                        xpos sx + 48
                        ypos sy + 48
                        size 20
                        color "#FFFFFF"
                        outlines [(2, "#00000088")]

        # Close button
        textbutton "Close":
            xpos 1650
            ypos 100
            action Hide("inventory")
