# journal_ui.rpy

################################################################################
## # Purpose: Journal UI screen and inputs
################################################################################

screen journal_ui():

    tag menu
    modal True
    zorder 100

    # ------------------------------
    # Base book background
    # ------------------------------
    # Replace with another base image if needed.
    add "images/journal/Book_Background_70ms.png"

    # ------------------------------
    # Page-turn overlay animation
    # ------------------------------
    # Controlled by journal_turning flag.
    if journal_turning:
        add "journal_page_turn"

    # ------------------------------
    # Tab buttons
    # ------------------------------
    # Move xpos/ypos to reposition tabs.
    vbox:
        xpos 150
        ypos 120
        spacing 10
        textbutton "Lore" action [SetVariable("journal_tab", "lore"), SetVariable("journal_page", 0)]
        textbutton "Quests" action [SetVariable("journal_tab", "quests"), SetVariable("journal_page", 0)]
        textbutton "Clues" action [SetVariable("journal_tab", "clues"), SetVariable("journal_page", 0)]

    # ------------------------------
    # Pull entries for current tab
    # ------------------------------
    $ entries = journal_get_entries()

    # ------------------------------
    # Content block
    # ------------------------------
    # Adjust text positions and sizes to fit the book art.
    if entries:
        $ entry = entries[journal_page % len(entries)]

        text entry["title"]:
            xpos 420
            ypos 220
            size 32
            color "#2b1b0e"

        text entry["text"]:
            xpos 420
            ypos 280
            xsize 600
            size 24
            color "#2b1b0e"
            line_spacing 6

    # ------------------------------
    # Navigation (Prev / Next)
    # ------------------------------
    # Timing control:
    # - Increase delay by adding renpy.pause(0.2) if needed.
    textbutton "Prev":
        xpos 380
        ypos 860
        action [
            SetVariable("journal_turning", True),
            SetVariable("journal_page", journal_page - 1),
            Function(renpy.restart_interaction),
            SetVariable("journal_turning", False)
        ]

    textbutton "Next":
        xpos 1100
        ypos 860
        action [
            SetVariable("journal_turning", True),
            SetVariable("journal_page", journal_page + 1),
            Function(renpy.restart_interaction),
            SetVariable("journal_turning", False)
        ]

    # ------------------------------
    # Close
    # ------------------------------
    textbutton "Close":
        xpos 1700
        ypos 80
        action Return()

# ------------------------------
# Key binding (J)
# ------------------------------
# Uses a custom key action to open the journal.
define config.keymap["journal"] = [ "K_j" ]

screen keymap():
    key "journal" action ShowMenu("journal_ui")
