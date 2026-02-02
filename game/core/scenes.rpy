# core/scenes.rpy
# Holds all location definitions and world navigation.
# This file defines the physical structure of the game world.
# It does NOT contain story logic, just spatial flow.

# ---------------------------------------------------------------------------
# Image Definitions (World Assets)
# ---------------------------------------------------------------------------
# These give us short, readable names in script.
# After this, we can use:
#   scene bg church exterior
# instead of long file paths.

# Church
image bg church exterior = "images/scenes/church/exterior_church.png"
image bg church interior = "images/scenes/church/interior_church.png"

# Gym
image bg gym exterior = "images/scenes/gym/exterior_gym.png"
image bg gym interior = "images/scenes/gym/interior_gym.png"

# Hotel
image bg hotel exterior = "images/scenes/hotel/exterior_hotel.png"
image bg hotel interior = "images/scenes/hotel/interior_hotel.png"

# Mall
image bg mall exterior = "images/scenes/mall/exterior_mall.png"
image bg mall interior = "images/scenes/mall/interior_mall.png"

# Psychic
image bg psychic exterior = "images/scenes/psychic/exterior_psychic.png"
image bg psychic interior = "images/scenes/psychic/interior_psychic.png"

# University
image bg university exterior = "images/scenes/university/exterior_university.png"
image bg university interior = "images/scenes/university/interior_university.png"

# Warehouse
image bg warehouse exterior = "images/scenes/warehouse/exterior_warehouse.png"
image bg warehouse interior = "images/scenes/warehouse/interior_warehouse.png"

# Private Investigator Office
image bg pi_office exterior = "images/scenes/pi_office/exterior_office_pi.png"
image bg pi_office interior = "images/scenes/pi_office/interior_office_pi.png"

# House (starter hub location, more granular than others)
image bg house exterior = "images/scenes/house/house_exterior.png"
image bg house entry    = "images/scenes/house/entry_way.png"
image bg house hallway  = "images/scenes/house/hallway.png"
image bg house kitchen  = "images/scenes/house/kitchen.png"
image bg house bathroom = "images/scenes/house/bathroom.png"
image bg house bedroom  = "images/scenes/house/bedroom_bg.png"


# ---------------------------------------------------------------------------
# World Navigation Helpers
# ---------------------------------------------------------------------------
# These labels define how the player moves through space.
# They should stay lightweight and reusable.
# Story content should live in story/ files, not here.

label go_map:
    # Central hub entry point.
    # Any system can jump here safely.
    call screen main_map
    return


# ---------------------------------------------------------------------------
# Location Loops (Spatial Flow Only)
# ---------------------------------------------------------------------------
# Each location follows a simple pattern:
#   exterior -> interior -> back to map
# Later, systems (journal, quests, sanity) can hook into these.


# -----------------
# Church
# -----------------

label church_exterior:
    scene bg church exterior
    "The church sits quiet."
    menu:
        "Go inside":
            jump church_interior
        "Back to map":
            jump go_map

label church_interior:
    scene bg church interior
    "It smells like old wood and dust."
    menu:
        "Back outside":
            jump church_exterior
        "Back to map":
            jump go_map


# -----------------
# Gym
# -----------------

label gym_exterior:
    scene bg gym exterior
    "The gym looks abandoned."
    menu:
        "Go inside":
            jump gym_interior
        "Back to map":
            jump go_map

label gym_interior:
    scene bg gym interior
    "The air is stale and heavy."
    menu:
        "Back outside":
            jump gym_exterior
        "Back to map":
            jump go_map


# -----------------
# House (starter hub)
# -----------------
# The house is more detailed and will likely grow into
# a small internal navigation map later.

label house_exterior:
    scene bg house exterior
    "Home doesn't feel safe anymore."
    menu:
        "Go inside":
            jump house_entry
        "Back to map":
            jump go_map

label house_entry:
    scene bg house entry
    menu:
        "Hallway":
            jump house_hallway
        "Back outside":
            jump house_exterior

label house_hallway:
    scene bg house hallway
    menu:
        "Kitchen":
            jump house_kitchen
        "Bathroom":
            jump house_bathroom
        "Bedroom":
            jump house_bedroom
        "Back to entry":
            jump house_entry

label house_kitchen:
    scene bg house kitchen
    "The kitchen feels cold."
    menu:
        "Back to hallway":
            jump house_hallway

label house_bathroom:
    scene bg house bathroom
    "The mirror makes you uneasy."
    menu:
        "Back to hallway":
            jump house_hallway

label house_bedroom:
    scene bg house bedroom
    "Your room. It should feel safe."
    menu:
        "Back to hallway":
            jump house_hallway
