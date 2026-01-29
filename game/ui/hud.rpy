# hud.rpy

################################################################################
## Holds HUD state, helper functions, and small data tables.
################################################################################

# ---------------------------------------------------------------------------
# HUD Placement Config (edit THESE numbers)
# ---------------------------------------------------------------------------

define HUD_POS = {
    "player_status_border": (325, 0.70),
    "equipment_border":     (1650, 0.70),
    "icon_border":          (20, 0.70),

    "player_logo":          (40, 0.70),
    "player_logo_size":     (285, 310),

    "heartbeat":            (31, 0.03),

    "sanity_group":         (115, 0.05),

    "status_row":           (350, 0.765),
    "status_spacing":       20,

    "tooltip":              (380, 0.86),

    "buttons_group":        (31, 0.15),
    "buttons_spacing":      14,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Helpers are small functions that read game data and return something useful for the UI.
# They do not change game state or make decisions, which keeps them safe and predictable.
# They exist so the HUD can stay clean without mixing visuals and game logic.

init -2 python:

    def player_logo():
        path = f"images/hud/icons/{player_gender}_{player_race}_{player_outfit}_{player_emotion}_{player_body}_logo.png"
        if renpy.loadable(path):
            return path

        fallback = f"images/hud/icons/{player_gender}_{player_race}_{player_outfit}_idle_{player_body}_logo.png"
        if renpy.loadable(fallback):
            return fallback

        renpy.log(f"Missing HUD logo: {path}")
        return "gui/missing.png"

    def hb_delay():
        s = clamp(store.sanity, 0, store.sanity_max)
        if s >= 75:
            return 0.55
        elif s >= 50:
            return 0.40
        elif s >= 25:
            return 0.28
        else:
            return 0.18

    def safe_show(screen_name):
        if renpy.has_screen(screen_name):
            renpy.show_screen(screen_name)
        else:
            renpy.notify(f"{screen_name} screen not implemented.")

    def hud_should_show():
        if not getattr(store, "hud_visible", False):
            return False
        if renpy.get_screen("character_creation"):
            return False
        if renpy.get_screen("pause"):
            return False
        if renpy.get_screen("inventory"):
            return False
        return True


# ---------------------------------------------------------------------------
# Heartbeat Animation
# ---------------------------------------------------------------------------

image hud_heartbeat:
    "images/hud/heartbeat_1.png"
    pause hb_delay()
    "images/hud/heartbeat_2.png"
    pause hb_delay()
    "images/hud/heartbeat_3.png"
    pause hb_delay()
    "images/hud/heartbeat_4.png"
    pause hb_delay()
    repeat


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

style sanity_bar:
    xsize 420
    ysize 42

# ---------------------------------------------------------------------------
# HUD Screen
# ---------------------------------------------------------------------------


screen hud_display():
    modal False
    zorder 10

    default hud_tip = ""

    if hud_should_show():

        # Pull layout values
        $ psb_x, psb_y = HUD_POS["player_status_border"]
        $ eq_x,  eq_y  = HUD_POS["equipment_border"]
        $ ib_x,  ib_y  = HUD_POS["icon_border"]

        $ logo_x, logo_y = HUD_POS["player_logo"]
        $ logo_w, logo_h = HUD_POS["player_logo_size"]

        $ hb_x, hb_y = HUD_POS["heartbeat"]
        $ san_x, san_y = HUD_POS["sanity_group"]

        $ st_x, st_y = HUD_POS["status_row"]
        $ st_spacing = HUD_POS["status_spacing"]

        $ tip_x, tip_y = HUD_POS["tooltip"]

        $ btn_x, btn_y = HUD_POS["buttons_group"]
        $ btn_spacing = HUD_POS["buttons_spacing"]

        fixed:

            # Frames
            add "images/hud/player_status_border.png" xpos psb_x ypos psb_y
            add "images/hud/equipment_border.png"     xpos eq_x  ypos eq_y
            add "images/hud/icon_border.png"          xpos ib_x  ypos ib_y

            # Player logo
            add DynamicImage(player_logo()) size (logo_w, logo_h) xpos logo_x ypos logo_y

            # Heartbeat
            add "hud_heartbeat" xpos hb_x ypos hb_y

            # -------------------------
            # Sanity bar (fills behind)
            # -------------------------

            fixed:
                xpos san_x
                ypos san_y

                # Smooth display value
                $ sanity_display += (sanity - sanity_display) * 1.0

                $ pct = clamp(sanity_display / float(max(1, sanity_max)), 0.0, 1.0)
                $ fill_w = int(HUD_SANITY["fill_w"] * pct)

                # Green fill FIRST
                add Solid(
                    HUD_SANITY["fill_color"],
                    xsize=fill_w,
                    ysize=HUD_SANITY["fill_h"]
                ):
                    xpos HUD_SANITY["fill_x"]
                    ypos HUD_SANITY["fill_y"]

                # Frame LAST
                add "images/hud/sanity_bar_bg.png"

            # Status icons
            hbox:
                xpos st_x
                ypos st_y
                spacing st_spacing

                for s in player_statuses:
                    imagebutton:
                        idle  "images/hud/status/status_icon_%s.png" % s
                        hover "images/hud/status/status_icon_%s.png" % s
                        action NullAction()
                        hovered SetScreenVariable("hud_tip", STATUS_LABELS.get(s, s))
                        unhovered SetScreenVariable("hud_tip", "")

            # Tooltip
            if hud_tip:
                text hud_tip:
                    xpos tip_x
                    ypos tip_y
                    size 22
                    color "#FFFFFF"
                    outlines [(2, "#000000AA")]

            # Buttons
            vbox:
                xpos btn_x
                ypos btn_y
                spacing btn_spacing

                imagebutton:
                    idle  "images/hud/inventory_button.png"
                    hover "images/hud/inventory_button.png"
                    action Function(safe_show, "inventory")

                imagebutton:
                    idle  "images/hud/map_button.png"
                    hover "images/hud/map_button.png"
                    action Function(safe_show, "main_map")

                imagebutton:
                    idle  "images/hud/phone_button.png"
                    hover "images/hud/phone_button.png"
                    action Function(safe_show, "phone_home")