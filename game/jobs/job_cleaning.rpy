# jobs/job_cleaning.rpy
# Cleaning / janitorial: hidden-object search

label job_cleaning_play(job_state):
    $ shift = job_state["shift"]
    $ mg = renpy.call_screen("mg_hidden_object", job_state=job_state)
    $ success = bool(mg.get("success"))

    # Lore: small chance to reveal one lore hit; boost on success
    $ lore_hit = maybe_lore(shift, chance=0.45 if success else 0.20)
    $ lore_hits = [lore_hit] if lore_hit else []

    if success:
        $ notes = [
            "You finish the last corner and the room finally looks like it belongs to this year.",
            "Something about the air still feels staged.",
        ]
    else:
        $ notes = [
            "You run out of time and leave a few things exactly where someone wanted them.",
        ]

    return {"success": success, "lore_hits": lore_hits, "notes": notes}
