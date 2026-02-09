# jobs/job_content.rpy
# Content lives here: add shifts without touching the engine.
# Coordinates assume 1280x720. If you use a different resolution, scale accordingly.

# For prototypes, bg can be Solid colors. Replace with images later.

init -2 python:
    # --- Cleaning (Hidden Object)
    CLEANING_SHIFTS = [
        {
            "id": "clean_apt_01",
            "title": "Apartment Turnover",
            "bg": Solid("#111"),
            "time_limit": 20.0,
            "items": [
                {"name": "keyring", "x": 180, "y": 420, "w": 80, "h": 60},
                {"name": "photo_frame", "x": 760, "y": 280, "w": 110, "h": 90},
                {"name": "receipt", "x": 520, "y": 610, "w": 90, "h": 55},
                {"name": "glove", "x": 950, "y": 520, "w": 90, "h": 60},
            ],
            "lore": ["symbol_on_glove", "receipt_oldtown_address"],
            "npc": "Landlord Bryce",
            "mods": ["distraction", "short_timer"],
            "distraction_text": "A neighbor asks if you \"heard the water\" last night.",
        },
        {
            "id": "clean_motel_02",
            "title": "Motel Room 6",
            "bg": Solid("#141016"),
            "time_limit": 18.0,
            "items": [
                {"name": "stain_kit", "x": 240, "y": 610, "w": 120, "h": 55},
                {"name": "phone", "x": 820, "y": 460, "w": 90, "h": 70},
                {"name": "flyer", "x": 620, "y": 260, "w": 110, "h": 80},
            ],
            "lore": ["flyer_1987"],
            "mods": ["short_timer"],
            "distraction_text": "The TV turns on by itself. Static, then a weather report for a year that isn't this one.",
        },
    ]

    # --- Landscaping (Anomaly Spot)
    LANDSCAPING_SHIFTS = [
        {
            "id": "land_yard_01",
            "title": "Yard Trim on Fourth Street",
            "bg": Solid("#0b1a10"),
            "time_limit": 16.0,
            "anomalies": [
                {"name": "beetle", "x": 260, "y": 520, "w": 60, "h": 40},
                {"name": "root_mark", "x": 860, "y": 560, "w": 90, "h": 60},
                {"name": "odd_soil", "x": 540, "y": 410, "w": 90, "h": 60},
            ],
            "lore": ["symbol_in_root", "gps_deadend_4th"],
            "mods": ["distraction"],
            "distraction_text": "You keep trimming the same hedge, but the clippings never pile up.",
        },
        {
            "id": "land_park_02",
            "title": "Park Bed Replanting",
            "bg": Solid("#0d1f13"),
            "time_limit": 18.0,
            "anomalies": [
                {"name": "worm_knot", "x": 420, "y": 610, "w": 80, "h": 50},
                {"name": "rusted_tag", "x": 780, "y": 500, "w": 80, "h": 50},
            ],
            "lore": ["park_banner_1987"],
            "mods": ["short_timer"],
            "distraction_text": "A squirrel drops a soggy paper tag at your feet, like it's delivering evidence.",
        },
    ]

    # --- Delivery (Reaction Window)
    DELIVERY_SHIFTS = [
        {
            "id": "del_burrito_01",
            "title": "Burrito Run",
            "bg": Solid("#101018"),
            "rounds": 6,
            "window": 0.75,
            "min_wait": 0.7,
            "max_wait": 2.2,
            "lore": ["double_street_sign"],
            "mods": ["double_pay"],
        },
        {
            "id": "del_pharmacy_02",
            "title": "Pharmacy Courier",
            "bg": Solid("#0f121a"),
            "rounds": 7,
            "window": 0.65,
            "min_wait": 0.6,
            "max_wait": 1.9,
            "lore": ["mailroom_blacklist"],
            "mods": ["short_timer", "double_pay"],
        },
    ]

    # --- Nursing Home (Dialogue + Memory)
    NURSING_SHIFTS = [
        {
            "id": "nurse_evening_01",
            "title": "Evening Rounds",
            "bg": Solid("#0f1012"),
            "start_trust": 2,
            "pass_trust": 3,
            "beats": [
                {
                    "line": "Resident: \"Are we still in the old place?\"",
                    "options": [
                        {"text": "We’re safe here. Want some water?", "trust_delta": 1},
                        {"text": "What do you mean by old place?", "trust_delta": 0},
                        {"text": "Try to sleep. It’s late.", "trust_delta": -1},
                    ],
                },
                {
                    "line": "Resident: \"The river took the streets, but not the names.\"",
                    "options": [
                        {"text": "Tell me a street name you remember.", "trust_delta": 1},
                        {"text": "That sounds like a dream.", "trust_delta": -1},
                    ],
                },
            ],
            "pairs": [("Rose", "Rose"), ("Key", "Key"), ("Map", "Map"), ("Badge", "Badge")],
            "lore": ["archive_gap", "address_echo"],
            "mods": ["distraction"],
        },
    ]

    # --- Creative Contract (Poster Builder; RenPyDraw-friendly placeholder)
    CREATIVE_SHIFTS = [
        {
            "id": "art_flyer_01",
            "title": "Community Flyer",
            "requirements": ["include: symbol", "tone: cheerful"],
            "poster_bgs": ["poster_bg_1", "poster_bg_2"],
            "poster_parts": ["symbol", "flower", "moon", "ribbon"],
            "lore": ["symbol_requested_logo"],
            "mods": ["double_pay"],
        },
    ]
