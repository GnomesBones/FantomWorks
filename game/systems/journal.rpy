################################################################################
# journal.rpy
# Purpose: Journal data + page-turn animation + helpers
################################################################################

# ------------------------------
# Page-turn animation (13 frames)
# ------------------------------
# Adjust frame order, timing (0.03), or add/remove frames.
# The names below match the provided files.
image journal_page_turn:
    "images/journal/Book_Frame 2.png"
    0.03
    "images/journal/Book_Frame 3.png"
    0.03
    "images/journal/Book_Frame 4.png"
    0.03
    "images/journal/Book_Frame 5.png"
    0.03
    "images/journal/Book_Frame 6.png"
    0.03
    "images/journal/Book_Frame 7.png"
    0.03
    "images/journal/Book_Frame 8.png"
    0.03
    "images/journal/Book_Frame 9.png"
    0.03
    "images/journal/Book_Frame 10.png"
    0.03
    "images/journal/Book_Frame 11.png"
    0.03
    "images/journal/Book_Frame 12.png"
    0.03
    "images/journal/Book_Frame 13.png"
    0.03
    repeat

# ------------------------------
# Journal state (defaults)
# ------------------------------
# journal_tab: which category is shown.
# journal_page: index into the current category list.
# journal_turning: controls whether the page-turn animation is visible.
default journal_tab = "lore"
default journal_page = 0
default journal_turning = False

# ------------------------------
# Data lists (entries)
# ------------------------------
# Each entry: title, text, unlocked (bool).
# Add or remove entries freely.
default lore_entries = [
    {"title": "The Mirror", "text": "It watches back.", "unlocked": True},
    {"title": "The Well", "text": "Cold air rises.", "unlocked": False},
]

default quest_entries = [
    {"title": "Meet the Team", "text": "Talk to the people who replied.", "unlocked": True},
]

default clue_entries = [
    {"title": "EMF Spike", "text": "EMF level 4 in the hallway.", "unlocked": True},
]

# ------------------------------
# Helper: get the current list
# ------------------------------
# Returns only unlocked entries based on the current tab.
# Adjust categories here if more tabs are added.
init python:
    def journal_get_entries():
        if store.journal_tab == "lore":
            return [e for e in store.lore_entries if e["unlocked"]]
        elif store.journal_tab == "quests":
            return [e for e in store.quest_entries if e["unlocked"]]
        else:
            return [e for e in store.clue_entries if e["unlocked"]]
