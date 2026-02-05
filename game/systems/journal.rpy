################################################################################
# game/systems/journal.rpy
#
# Purpose:
# - Journal data (lore, quests, clues)
# - Page-turn animation
# - Helpers that return the correct pages for the journal UI
#
# Quests tab:
# - Uses live data from game/systems/objectives.rpy
# - No manual quest_entries list needed
################################################################################


# ------------------------------------------------------------------------------
# Page-turn animation (13 frames)
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Journal state (defaults)
# ------------------------------------------------------------------------------
# journal_tab: which category is shown.
# journal_page: index into the current category list.
# journal_turning: controls whether the page-turn animation is visible.
default journal_tab = "lore"
default journal_page = 0
default journal_turning = False


# ------------------------------------------------------------------------------
# Data lists (entries)
# ------------------------------------------------------------------------------
# Each entry: title, text, unlocked (bool).
# Add or remove entries freely.
default lore_entries = [
    {"title": "The Mirror", "text": "It watches back.", "unlocked": True},
    {"title": "The Well", "text": "Cold air rises.", "unlocked": False},
]

default clue_entries = [
    {"title": "EMF Spike", "text": "EMF level 4 in the hallway.", "unlocked": True},
]

# NOTE (important change):
# Manual quest_entries has been removed.
# Quests are generated live from objectives.rpy.


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
init python:

    def journal_get_quest_pages():
        """
        Builds quest pages from the Objective Manager.

        Output format:
        [
            { "title": "...", "text": "..." },
            ...
        ]
        """
        pages = []

        # 1) Pinned objective first (matches HUD)
        pinned = obj_find_pinned_step_info()
        if pinned and pinned.get("text"):
            pages.append({
                "title": "Pinned Objective",
                "text": pinned["text"],
            })

        # 2) Quests grouped by type
        type_labels = [
            ("investigative", "Investigations"),
            ("character_arc", "Character Arcs"),
            ("player_progression", "Progression"),
            ("ghost_arc", "Ghost Arcs"),
        ]

        for qtype, label in type_labels:
            quest_ids = obj_list_quests_by_type(qtype)

            for qid in quest_ids:
                q = QUESTS.get(qid, None)
                if not q:
                    continue

                done, total, mandatory_remaining = obj_quest_progress(qid)

                # Build step list text
                lines = []
                for s in obj_quest_steps(qid):
                    mark = "x" if s["done"] else " "
                    opt = "" if s["mandatory"] else " (Optional)"
                    lines.append(f"[{mark}] {s['text']}{opt}")

                desc = q.get("description", "").strip()
                header = f"Progress: {done}/{total}   Mandatory left: {mandatory_remaining}".strip()

                body_parts = []
                if desc:
                    body_parts.append(desc)
                body_parts.append(header)
                body_parts.append("")
                body_parts.append("\n".join(lines))

                pages.append({
                    "title": f"{label}: {q.get('title', '')}",
                    "text": "\n\n".join([p for p in body_parts if p is not None]).strip(),
                })

        return pages


    def journal_get_entries():
        """
        Returns only unlocked entries based on the current tab.

        Tabs:
        - lore: from lore_entries
        - quests: live pages from objectives.rpy
        - clues: from clue_entries
        """
        if store.journal_tab == "lore":
            return [e for e in store.lore_entries if e.get("unlocked", False)]

        elif store.journal_tab == "quests":
            pages = journal_get_quest_pages()

            # Convert to the same shape used by journal_ui.rpy
            return [
                {"title": p["title"], "text": p["text"], "unlocked": True}
                for p in pages
            ]

        else:
            return [e for e in store.clue_entries if e.get("unlocked", False)]
