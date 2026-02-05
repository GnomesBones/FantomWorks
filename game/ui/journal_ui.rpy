################################################################################
# game/ui/journal_ui.rpy
#
# Purpose:
# - Journal UI screen
# - Simple page turning (Prev/Next)
# - Tabs: Lore / Quests / Clues
#
# Notes:
# - Page turn animation uses journal_turning flag.
# - Entries come from journal_get_entries() in systems/journal.rpy
# - substitute False prevents Ren'Py from treating [brackets] as interpolation.
################################################################################

screen journal_ui():

    tag menu
    modal True
    zorder 100

    # --------------------------------------------------------------------------
    # Base book background
    # --------------------------------------------------------------------------
    add "images/journal/Book_Background_70ms.png" xalign 0.5 yalign 0.5 xsize config.screen_width ysize config.screen_height

    # --------------------------------------------------------------------------
    # Page-turn overlay animation
    # --------------------------------------------------------------------------
    if journal_turning:
        add "journal_page_turn"

    # --------------------------------------------------------------------------
    # Tabs (simple buttons for now)
    # --------------------------------------------------------------------------
    vbox:
        xpos 150
        ypos 120
        spacing 10

        textbutton "Lore" action [
            SetVariable("journal_tab", "lore"),
            SetVariable("journal_page", 0),
        ]

        textbutton "Quests" action [
            SetVariable("journal_tab", "quests"),
            SetVariable("journal_page", 0),
        ]

        textbutton "Clues" action [
            SetVariable("journal_tab", "clues"),
            SetVariable("journal_page", 0),
        ]

    # --------------------------------------------------------------------------
    # Pull entries for current tab
    # --------------------------------------------------------------------------
    $ entries = journal_get_entries()

    # --------------------------------------------------------------------------
    # Content block
    # --------------------------------------------------------------------------
    if entries:
        $ entry = entries[journal_page % len(entries)]

        text entry["title"]:
            xpos 420
            ypos 220
            size 32
            color "#2b1b0e"
            substitute False

        # Use a viewport so long pages do not get cut off.
        viewport:
            xpos 420
            ypos 280
            xsize 900
            ysize 560
            mousewheel True
            draggable True

            text entry["text"]:
                size 24
                color "#2b1b0e"
                line_spacing 6
                substitute False

    else:
        text "Nothing here yet.":
            xpos 420
            ypos 280
            size 28
            color "#2b1b0e"

    # --------------------------------------------------------------------------
    # Page navigation (simple)
    # --------------------------------------------------------------------------
    textbutton "< Prev":
        xpos 380
        ypos 860
        sensitive (len(entries) > 1)
        action [
            SetVariable("journal_turning", True),
            SetVariable("journal_page", journal_page - 1),
            Function(renpy.restart_interaction),
            SetVariable("journal_turning", False),
        ]

    textbutton "Next >":
        xpos 1100
        ypos 860
        sensitive (len(entries) > 1)
        action [
            SetVariable("journal_turning", True),
            SetVariable("journal_page", journal_page + 1),
            Function(renpy.restart_interaction),
            SetVariable("journal_turning", False),
        ]

    # --------------------------------------------------------------------------
    # Close
    # --------------------------------------------------------------------------
    textbutton "Close":
        xpos 1700
        ypos 80
        action Return()


################################################################################
# Key binding (J)
################################################################################

init python:
    config.keymap["journal"] = [ "K_j" ]

screen keymap():
    key "journal" action ShowMenu("journal_ui")
