# party_system.rpy
# Pick up to 3 teammates for a mission.

# Current selected mission party
default party = []              # example: ["the_detective", "the_psychic", "the_priest"]
default party_limit = 3

# Optional: track availability (unlocking teammates as story progresses)
default roster_unlocked = set([
    "the_detective",
    "the_psychic",
    "the_researcher",
    "the_exorcist",
    "the_jock",
    "the_priest",
])

init python:

    def party_is_full():
        return len(party) >= party_limit

    def party_has(k):
        return k in party

    def party_add(k):
        # Only add if unlocked, not already in, and not full
        if k in roster_unlocked and k not in party and not party_is_full():
            party.append(k)
            return True
        return False

    def party_remove(k):
        if k in party:
            party.remove(k)
            return True
        return False

    def party_clear():
        party[:] = []


##############################################################################
# Screen: Party Selection
##############################################################################

screen party_select():
    tag menu

    vbox:
        spacing 10

        text "Choose 3 teammates"

        # Selected team display
        hbox:
            spacing 10
            text "Selected: [len(party)] / [party_limit]"
            if len(party) > 0:
                text " | "
                text ", ".join([team[k]["meta"]["name"] for k in party])

        # Show roster buttons
        for k in team.keys():
            if k in roster_unlocked:
                $ name = team[k]["meta"]["name"]

                hbox:
                    spacing 10

                    # Toggle button
                    if k in party:
                        textbutton "Remove" action Function(party_remove, k)
                    else:
                        # Disable add button if full
                        if len(party) >= party_limit:
                            textbutton "Add" action NullAction()
                        else:
                            textbutton "Add" action Function(party_add, k)

                    text "[name]"

        null height 10

        # Actions
        hbox:
            spacing 10
            textbutton "Clear" action Function(party_clear)
            textbutton "Back" action Return()

        # Start mission only when exactly 3 selected
        if len(party) == party_limit:
            textbutton "Confirm Team" action Return(True)
        else:
            text "Pick exactly 3 to continue."


##############################################################################
# Mission flow
##############################################################################

label choose_team_for_mission:

    # Clear old picks each mission (optional)
    $ party_clear()

    # Open selection UI
    $ ok = call screen party_select

    # If closed without confirm, ok may be None
    if ok is True and len(party) == party_limit:
        return
    else:
        # Re-open until a valid team is chosen
        jump choose_team_for_mission


label start_mission_example:
    call choose_team_for_mission

    # Now party always has exactly 3 keys
    "Team chosen: [team[party[0]]['meta']['name']], [team[party[1]]['meta']['name']], [team[party[2]]['meta']['name']]."

    # Example: conditional lines
    if "the_psychic" in party:
        PSYCHIC "Lavender first. Rules are rules."

    if "the_detective" in party:
        DETECTIVE "Noir rule number one: never trust a doll."

    # Continue mission...
    return
