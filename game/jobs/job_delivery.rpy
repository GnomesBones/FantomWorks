# jobs/job_delivery.rpy
# Courier / delivery: reaction time window

label job_delivery_play(job_state):
    $ shift = job_state["shift"]
    $ mg = renpy.call_screen("mg_reaction_window", job_state=job_state)
    $ success = bool(mg.get("success"))

    $ lore_hit = maybe_lore(shift, chance=0.35 if success else 0.10)
    $ lore_hits = [lore_hit] if lore_hit else []

    if success:
        $ notes = [
            "You make the last turn on instinct and somehow it is the right street.",
            "The tip is decent. The address is… questionable.",
        ]
    else:
        $ notes = [
            "You miss a beat, then another. The town punishes hesitation.",
        ]

    return {"success": success, "lore_hits": lore_hits, "notes": notes}
