################################################################################
# game/ui/hud.rpy
#
# Purpose:
# - HUD state + helpers
# - HUD screen (always behind menus)
# - Quick buttons (inventory, map, journal, phone)
#
# Key idea:
# - HUD stays visible during gameplay.
# - When a menu screen opens (journal, pause, inventory), that menu sits on top.
# - HUD can either keep drawing underneath, or be hidden while menus are open.
#   This file keeps HUD drawing underneath (behind) by using zorder and by NOT
#   hiding it in hud_should_show().
################################################################################

# ---------------------------------------------------------------------------
# HUD Placement Config (edit THESE numbers)
# ---------------------------------------------------------------------------

define HUD_POS = {
    "objective_text":      (1250, 0.05),

    "player_status_border": (325, 0.60),
    "equipment_border":     (1650, 0.70),
    "icon_border":          (20, 0.70),

    "player_logo":          (40, 0.70),
    "player_logo_size":     (285, 310),

    "heartbeat":            (31, 0.03),

    "sanity_group":         (115, 0.05),

    "status_row":           (350, 0.665),
    "status_spacing":       20,

    "tooltip":              (380, 0.86),

    "buttons_group":        (31, 0.15),
    "buttons_spacing":      14,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
        """
        Only use this for non-menu overlay screens.
        Journal is a menu screen, so it should use ShowMenu("journal_ui") instead.
        """
        if renpy.has_screen(screen_name):
            renpy.show_screen(screen_name)
        else:
            renpy.notify(f"{screen_name} screen not implemented.")

    def hud_should_show():
        """
        HUD stays available during gameplay.
        Menu screens appear above it, so it can stay "behind" without being hidden.
        Keep the exclusions only for screens that would visually clash.
        """
        if not getattr(store, "hud_visible", False):
            return False

        # Hide HUD while dialogue is happening.
        # Works for ADV/NVL dialogue, menus, and narration screens.
        if renpy.get_screen("say") or renpy.get_screen("nvl"):
            return False

        # Hide during character creation so the UI is clean.
        if renpy.get_screen("character_creation"):
            return False

        # If these menu screens should NOT show HUD underneath, keep these.
        # To keep HUD behind everything, remove these checks.
        if renpy.get_screen("pause"):
            return False
        if renpy.get_screen("inventory"):
            return False

        # Journal is a menu and will sit on top anyway.
        # HUD can stay behind it, so no need to hide here.

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
# Ghost Animation
# ---------------------------------------------------------------------------

image ghost_chase:
    "images/hud/HUD_ghost.png"

transform ghost_swoop:
    xalign -0.2 yalign 0.05 alpha 1.0
    linear 1.2 xalign 1.2 alpha 0.0


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

    # HUD zorder should be LOWER than menu screens like journal_ui (zorder 100).
    # 10 is fine, it will stay behind.
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
            # Sanity bar
            # -------------------------
            fixed:
                xpos san_x
                ypos san_y

                # Smooth display value (sanity_display should exist in player_state/game_state)
                $ sanity_display += (sanity - sanity_display) * 1.0

                $ pct = clamp(sanity_display / float(max(1, sanity_max)), 0.0, 1.0)
                $ fill_w = int(HUD_SANITY["fill_w"] * pct)

                add Solid(
                    HUD_SANITY["fill_color"],
                    xsize=fill_w,
                    ysize=HUD_SANITY["fill_h"]
                ):
                    xpos HUD_SANITY["fill_x"]
                    ypos HUD_SANITY["fill_y"]

                add "images/hud/sanity_bar_bg.png"

            # -------------------------
            # Status icons
            # -------------------------
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

            # -------------------------
            # Objective text
            # -------------------------
            $ obj_x, obj_y = HUD_POS["objective_text"]

            text "Objective: [obj_current_text()]":
                xpos obj_x
                ypos obj_y
                size 24
                color "#FFFFFF"
                outlines [(2, "#000000AA")]

            # -------------------------
            # Buttons
            # -------------------------
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

                # Journal is a menu screen named "journal_ui"
                imagebutton:
                    idle  "images/hud/journal_button.png"
                    hover "images/hud/journal_button.png"
                    action ShowMenu("journal_ui")

                imagebutton:
                    idle  "images/hud/phone_button.png"
                    hover "images/hud/phone_button.png"
                    action Function(safe_show, "phone_home")


# ---------------------------------------------------------------------------
# Objective Complete FX
# ---------------------------------------------------------------------------

screen objective_complete_fx(text_to_chase):
    zorder 200
    modal False

    text text_to_chase:
        xpos 1250
        ypos 0.05
        size 24
        color "#FFFFFF"
        outlines [(2, "#000000AA")]
        at Move((0, 0.05), (0.9, 0.05), 1.2, xanchor=0.0, yanchor=0.0)

    add "ghost_chase" at ghost_swoop

    timer 1.3 action Hide("objective_complete_fx")


label objective_complete_fx_show(text_to_show=""):
    show screen objective_complete_fx(text_to_chase=text_to_show)
    $ renpy.pause(1.2, hard=True)
    hide screen objective_complete_fx
    return
