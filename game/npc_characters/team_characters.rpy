# team_characters.rpy
# Data only. No scenes. No dialogue labels.
# Goal: One clean database for all team characters.
#
# Editing rules:
# - Add new stats/abilities/status keys to EVERY character to keep the schema consistent.
# - Keep this file as a "filing cabinet". Put gameplay logic in system files.

##############################################################################
# 1) TEAM DATABASE
# Add or edit characters here.
##############################################################################

default team = {

    # ======================================================================
    # THE DETECTIVE
    # ======================================================================
    "the_detective": {
        # Identity and writing flavor
        "meta": {
            # Alter: change name string
            "name": "Detective Lena Hart",

            # Alter: set pronouns for text formatting
            "pronouns": {"subj":"she", "obj":"her", "pos":"her"},

            # Alter: optional UI color for nameplates or menus
            "color": "#BBD2FF",

            # Alter: quick tags used for filtering or UI badges
            "archetype": "detective",
            "tone": "dry noir humor",
        },

        # Backstory and personality notes for easy reference
        "profile": {
            # Alter: rewrite as needed
            "backstory": "Joined after her shift. Joined the paranormal team to prove the supernatural is fake.",
            "fear": "Losing control in a situation that cannot be handled like an arrest. Deeply unsettled by dolls.",
            "motivation": "Claims the goal is to debunk nonsense.",
            "quirk": "Treats every case like a noir movie.",
        },

        # Art paths for menus, intros, profiles
        "art": {
            # Alter: update path if file name changes
            "intro": "npc_characters/team_characters/the_detective/detective_intro.png",

            # Alter: add more assets later
            # "profile": "npc_characters/team_characters/the_detective/detective_profile.png",
        },

        # Relationship data for dating sim logic
        "relationship": {
            # Alter: starting values
            "affection": 0,
            "trust": 0,
            "route": None,   # None / "friend" / "romance" / "locked"
        },

        # General stats used by checks, scenes, consequences
        "stats": {
            # Alter: tune ranges to match design
            "sanity": 100,
            "stress": 0,
            "courage": 2,

            # Alter: add more stats later for all characters, same keys
            "focus": 3,
            "charm": 1,
        },

        # Abilities for investigation systems
        "abilities": {
            # Alter: tune numbers
            "investigation": 3,
            "research": 2,
            "intuition": 1,
            "rituals": 0,
            "strength": 1,
        },

        # Equipment slots and containers
        "equipment": {
            # Alter: set to item ids later if an item system exists
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        # Status effects for ongoing conditions
        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,

            # Alter: add more statuses later for all characters
            "doll_shaken": False,
        },

        # One-time story markers
        "flags": set(),
    },


    # ======================================================================
    # THE PSYCHIC
    # ======================================================================
    "the_psychic": {
        "meta": {
            "name": "Ezra Moon",
            "pronouns": {"subj":"he", "obj":"him", "pos":"his"},
            "color": "#FFBDEB",
            "archetype": "psychic",
            "tone": "dramatic showman",
        },

        "profile": {
            "backstory": "Full-time psychic medium with a flair for the dramatic. Runs a YouTube channel with mixed reviews. Claims the gift came from a great-aunt. Possibly a fraud. Possibly haunted. Possibly both.",
            "fear": "That everything is imagined and the truth is just being weird. 'Allergic to ghosts' in a psychosomatic way.",
            "motivation": "Wants to prove legitimacy, especially to himself.",
            "quirk": "Smells lavender oil before entering a haunted room to 'center the soul.'",
        },

        "art": {
            "intro": "npc_characters/team_characters/the_psychic/psychic_intro.png",
        },

        "relationship": {
            "affection": 0,
            "trust": 0,
            "route": None,
        },

        "stats": {
            "sanity": 90,
            "stress": 0,
            "courage": 1,
            "focus": 1,
            "charm": 3,
        },

        "abilities": {
            "investigation": 1,
            "research": 1,
            "intuition": 3,
            "rituals": 2,
            "strength": 0,
        },

        "equipment": {
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,

            # Alter: use for ghost-allergy gag scenes or penalties
            "ghost_allergy": False,
        },

        "flags": set(),
    },


    # ======================================================================
    # THE RESEARCHER
    # ======================================================================
    "the_researcher": {
        "meta": {
            "name": "Dr. Riley Voss",
            "pronouns": {"subj":"they", "obj":"them", "pos":"their"},
            "color": "#B8FFF4",
            "archetype": "researcher",
            "tone": "clinical skeptic",
        },

        "profile": {
            "backstory": "Scientist from the local university. Started debunking ghost hunting as a thesis experiment and somehow got tenure out of it.",
            "fear": "Being proven wrong, especially by Ezra.",
            "motivation": "Wants hard evidence that supernatural phenomena can be quantified.",
            "quirk": "Carries a labeled field journal and refuses to acknowledge emotions without data.",
        },

        "art": {
            "intro": "npc_characters/team_characters/the_researcher/researcher_intro.png",
        },

        "relationship": {
            "affection": 0,
            "trust": 0,
            "route": None,
        },

        "stats": {
            "sanity": 105,
            "stress": 0,
            "courage": 1,
            "focus": 4,
            "charm": 0,
        },

        "abilities": {
            "investigation": 2,
            "research": 4,
            "intuition": 1,
            "rituals": 0,
            "strength": 0,
        },

        "equipment": {
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,
            "data_lock": False,
        },

        "flags": set(),
    },


    # ======================================================================
    # THE EXORCIST
    # ======================================================================
    "the_exorcist": {
        "meta": {
            "name": "Sister May Castella",
            "pronouns": {"subj":"she", "obj":"her", "pos":"her"},
            "color": "#FFD6A6",
            "archetype": "exorcist",
            "tone": "tired veteran",
        },

        "profile": {
            "backstory": "Technically retired from the Church. Prefers knitting or gardening but keeps getting dragged back in by escalating hauntings.",
            "fear": "Failing to stop real evil because being too old for this nonsense.",
            "motivation": "Does not want to be here, but refuses to let anyone get hurt on her watch.",
            "quirk": "Mutters Latin under her breath when annoyed. Carries a flask. Contents stay unasked.",
        },

        "art": {
            "intro": "npc_characters/team_characters/the_exorcist/exor_intro.png",
        },

        "relationship": {
            "affection": 0,
            "trust": 0,
            "route": None,
        },

        "stats": {
            "sanity": 110,
            "stress": 0,
            "courage": 3,
            "focus": 2,
            "charm": 1,
        },

        "abilities": {
            "investigation": 1,
            "research": 1,
            "intuition": 2,
            "rituals": 4,
            "strength": 1,
        },

        "equipment": {
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,
            "too_old_for_this": False,
        },

        "flags": set(),
    },


    # ======================================================================
    # THE JOCK
    # ======================================================================
    "the_jock": {
        "meta": {
            "name": "Brandon Steele",
            "pronouns": {"subj":"he", "obj":"him", "pos":"his"},
            "color": "#C7FFB8",
            "archetype": "jock",
            "tone": "big energy, low shame",
        },

        "profile": {
            "backstory": "Still wears the varsity jacket. Haunted the high school with a prank that backfired. Now calls ghost hunting a second career, first being high school quarterback.",
            "fear": "Looking stupid. Also basements.",
            "motivation": "Wants relevance and maybe a paranormal reality show deal.",
            "quirk": "Calls ghosts 'bros' and the EMF reader 'Coach.'",
        },

        "art": {
            "intro": "npc_characters/team_characters/the_jock/jock_intro.png",
        },

        "relationship": {
            "affection": 0,
            "trust": 0,
            "route": None,
        },

        "stats": {
            "sanity": 100,
            "stress": 0,
            "courage": 4,
            "focus": 1,
            "charm": 2,
        },

        "abilities": {
            "investigation": 1,
            "research": 0,
            "intuition": 1,
            "rituals": 0,
            "strength": 4,
        },

        "equipment": {
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,
            "basement_nerves": False,
        },

        "flags": set(),
    },


    # ======================================================================
    # THE PRIEST
    # ======================================================================
    "the_priest": {
        "meta": {
            "name": "Father Dominic \"Dom\" Reyes",
            "pronouns": {"subj":"he", "obj":"him", "pos":"his"},
            "color": "#FFF1B8",
            "archetype": "priest",
            "tone": "chill protector",
        },

        "profile": {
            "backstory": "Community pastor who moonlights as a ghost hunter because God helps those who help themselves... fight poltergeists.",
            "fear": "Accidentally offending something that cannot be prayed away.",
            "motivation": "Wants to help people, even the dead ones.",
            "quirk": "Holy water spray bottle. Bluetooth speaker plays gospel rap only.",
        },

        "art": {
            "intro": "npc_characters/team_characters/the_priest/priest_intro.png",
        },

        "relationship": {
            "affection": 0,
            "trust": 0,
            "route": None,
        },

        "stats": {
            "sanity": 110,
            "stress": 0,
            "courage": 2,
            "focus": 2,
            "charm": 2,
        },

        "abilities": {
            "investigation": 1,
            "research": 1,
            "intuition": 2,
            "rituals": 3,
            "strength": 1,
        },

        "equipment": {
            "primary": None,
            "secondary": None,
            "trinkets": [],
        },

        "status": {
            "injured": False,
            "haunted": False,
            "exhausted": False,
            "blessed": False,
        },

        "flags": set(),
    },
}


##############################################################################
# 2) OPTIONAL: SPEAKER OBJECTS FOR DIALOGUE
# Rename the left side identifiers if different speaking tags are preferred.
##############################################################################

# Speaker objects must not depend on default store variables like team.
# Keep these as constants.

define DETECTIVE  = Character("Detective Lena Hart", color="#BBD2FF")
define PSYCHIC    = Character("Ezra Moon",          color="#FFBDEB")
define RESEARCHER = Character("Dr. Riley Voss",     color="#B8FFF4")
define EXORCIST   = Character("Sister May Castella",color="#FFD6A6")
define JOCK       = Character("Brandon Steele",     color="#C7FFB8")
define PRIEST     = Character("Father Dominic \"Dom\" Reyes", color="#FFF1B8")


##############################################################################
# 3) GENERIC HELPERS
# These functions work for every teammate key.
##############################################################################

init python:

    # ------------------------------------------
    # Relationship helpers
    # ------------------------------------------

    def team_add_affection(k, amount=1):
        # Alter: change key names if relationship schema changes
        team[k]["relationship"]["affection"] += amount

    def team_add_trust(k, amount=1):
        team[k]["relationship"]["trust"] += amount

    def team_set_route(k, route_value):
        # None / "friend" / "romance" / "locked"
        team[k]["relationship"]["route"] = route_value


    # ------------------------------------------
    # Stats helpers
    # ------------------------------------------

    def team_add_stat(k, stat_key, amount=1):
        # Alter: add clamping here if needed (example: sanity 0..200)
        team[k]["stats"][stat_key] += amount

    def team_set_stat(k, stat_key, value):
        team[k]["stats"][stat_key] = value


    # ------------------------------------------
    # Status helpers
    # ------------------------------------------

    def team_set_status(k, status_key, value=True):
        team[k]["status"][status_key] = value

    def team_is_status(k, status_key):
        return bool(team[k]["status"].get(status_key, False))


    # ------------------------------------------
    # Flag helpers
    # ------------------------------------------

    def team_has_flag(k, flag):
        return flag in team[k]["flags"]

    def team_add_flag(k, flag):
        team[k]["flags"].add(flag)

    def team_remove_flag(k, flag):
        if flag in team[k]["flags"]:
            team[k]["flags"].remove(flag)


    # ------------------------------------------
    # Equipment helpers
    # ------------------------------------------

    def team_equip(k, slot, item_id):
        # slot: "primary" or "secondary"
        team[k]["equipment"][slot] = item_id

    def team_add_trinket(k, item_id):
        team[k]["equipment"]["trinkets"].append(item_id)

    def team_remove_trinket(k, item_id):
        tr = team[k]["equipment"]["trinkets"]
        if item_id in tr:
            tr.remove(item_id)


##############################################################################
# 4) EDITING NOTES
##############################################################################

# HOW TO ALTER CONTENT
#
# 1) Names
#    Edit: team["the_detective"]["meta"]["name"]
#
# 2) Pronouns
#    Edit: team["the_psychic"]["meta"]["pronouns"]
#    Keys are: subj / obj / pos
#
# 3) Stats and abilities
#    Edit numbers in:
#      team[k]["stats"]
#      team[k]["abilities"]
#
# 4) Add new stats, abilities, statuses
#    Add the same key to every character block.
#    Example new status:
#      "status": { ..., "cursed": False }
#
# 5) Art
#    Keep paths consistent with the folder layout.
#    If a file moves or gets renamed, update the string path.
#
# 6) Add new teammate
#    Copy one character block, paste, rename the key.
#    Keep sections: meta/profile/art/relationship/stats/abilities/equipment/status/flags
