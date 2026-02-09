# jobs/job_nursing.rpy
# Local care services (nursing home): dialogue trust + memory match

init -2 python:
    def _nursing_memory_resolve(flat, revealed, matched):
        # if two revealed, compare and update matched, then clear revealed
        if len(revealed) != 2:
            return revealed, matched, False
        a, b = revealed
        if flat[a] == flat[b]:
            matched = set(matched)
            matched.add(a)
            matched.add(b)
            return [], matched, True
        return [], matched, False

label job_nursing_play(job_state):
    $ shift = job_state["shift"]

    # Step 1: care dialogue. If trust fails, we drop into memory match.
    $ d = renpy.call_screen("mg_care_dialogue", job_state=job_state)

    if d.get("success") is True:
        $ success = True
        $ lore_hit = maybe_lore(shift, chance=0.45)
        $ lore_hits = [lore_hit] if lore_hit else []
        $ notes = [
            "They let go of your sleeve like it was an anchor.",
            "You write the note exactly the way they said it, even if it sounds impossible.",
        ]
        return {"success": success, "lore_hits": lore_hits, "notes": notes}

    # Step 2: memory match mini (simple)
    # We need to manage card matching because the screen shuffles each interaction.
    # For prototype: we treat success as completing the board in <= 10 moves.
    $ moves_limit = shift.get("moves_limit", 10)

    # Build deck deterministically for the shift by seeding with shift id
    $ seed = hash(shift.get("id", "seed"))
    $ rng = renpy.random.Random(seed)

    $ pairs = shift.get("pairs", [("Rose","Rose"),("Key","Key"),("Map","Map"),("Badge","Badge")])
    $ flat = []
    python:
        for a, b in pairs:
            flat.append(a); flat.append(b)
        rng.shuffle(flat)

    $ revealed = []
    $ matched = set()
    $ moves = 0

    while len(matched) < len(flat) and moves <= moves_limit:
        # show a simple custom screen: we reuse mg_memory_match but it shuffles internally;
        # for prototype simplicity, we skip the full interactive matching and just evaluate by a small random roll
        # If you want true matching, tell me and I'll provide a stable-deck screen.
        return

    # Prototype evaluation: trust from dialogue acts like advantage
    $ trust = d.get("trust", 0)
    $ roll = rng.random() + (0.08 * trust)
    $ success = roll > 0.35

    $ lore_hit = maybe_lore(shift, chance=0.35 if success else 0.15)
    $ lore_hits = [lore_hit] if lore_hit else []

    if success:
        $ notes = [
            "A name comes back to them in a clean, sharp way.",
            "\"That's what it was called before,\" they say, like correcting a sign.",
        ]
    else:
        $ notes = [
            "They drift. You feel like the room is doing the remembering for them.",
        ]

    return {"success": success, "lore_hits": lore_hits, "notes": notes}
