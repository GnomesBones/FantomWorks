# player_state.rpy

# Holds player stats and status effects.

# ---------------------------------------------------------------------------
# Helpers (keep core math helpers here so HUD doesn't redefine them)
# ---------------------------------------------------------------------------

init -2 python:
    def clamp(v, lo, hi):
        """
        Clamp v into [lo, hi].
        Works with ints and floats.
        """
        try:
            v = float(v)
        except:
            v = float(lo)
        return max(float(lo), min(float(hi), v))

# ---------------------------------------------------------------------------
# Sanity (game state)
# ---------------------------------------------------------------------------

default sanity = 100
default sanity_max = 100

# Used only for smoothing the HUD animation
default sanity_display = 100.0

# ---------------------------------------------------------------------------
# HUD sanity bar layout (HUD reads this, HUD does not own it)
# ---------------------------------------------------------------------------

define HUD_SANITY = {
    # Where the fill starts inside sanity_bar_bg.png
    "fill_x": 22,
    "fill_y": 8,

    # Full fill width when pct == 1.0
    "fill_w": 360,

    # Fill height
    "fill_h": 26,

    # Fill color for Solid()
    "fill_color": "#35C56A",
}

# ---------------------------------------------------------------------------
# Status effects (strings must match: status_icon_<name>.png)
# ---------------------------------------------------------------------------
# The strings must match filenames: status_icon_<name>.png


define STATUS_LIST = [
    "stressed",
    "bleeding_eyes",
    "confused",
    "dolls_curse",
    "doppelganger",
    "evp_echo",
    "frost",
    "hags_weight",
    "hexed",
    "mimic",
    "obsessed",
    "possessed",
    "scared",
    "shadow_touched",
]

# Optional: human-friendly names for UI tooltips
define STATUS_LABELS = {
    "stressed": "Stressed",
    "bleeding_eyes": "Bleeding Eyes",
    "confused": "Confused",
    "dolls_curse": "Doll's Curse",
    "doppelganger": "Doppelganger",
    "evp_echo": "EVP Echo",
    "frost": "Frost",
    "hags_weight": "Hag's Weight",
    "hexed": "Hexed",
    "mimic": "Mimic",
    "obsessed": "Obsessed",
    "possessed": "Possessed",
    "scared": "Scared",
    "shadow_touched": "Shadow Touched",
}

# Player’s current statuses (strings from STATUS_LIST)
default player_statuses = []



# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

init python:

    # ----- Status helpers -----

    def has_status(name):
        return name in store.player_statuses

    def add_status(name):
        if name not in STATUS_LIST:
            renpy.log("Unknown status: %s" % name)
            return
        if name not in player_statuses:
            player_statuses.append(name)

    def remove_status(name):
        if name in player_statuses:
            player_statuses.remove(name)

    def clear_statuses():
        player_statuses[:] = []


    # ----- Sanity helpers -----

    def change_sanity(amount, reason=None):
        store.sanity = clamp(store.sanity + amount, 0, store.sanity_max)

        if reason:
            renpy.log(f"Sanity change {amount}: {reason}")

    def lose_sanity(amount, reason=None):
        change_sanity(-abs(amount), reason)

    def restore_sanity(amount, reason=None):
        change_sanity(abs(amount), reason)
