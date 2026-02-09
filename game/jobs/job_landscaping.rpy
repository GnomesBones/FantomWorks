# jobs/job_landscaping.rpy
# Landscaping: anomaly spotting (find the bug / trip the hedge)

label job_landscaping_play(job_state):
    $ shift = job_state["shift"]
    $ mg = renpy.call_screen("mg_anomaly_spot", job_state=job_state)
    $ success = bool(mg.get("success"))

    $ lore_hit = maybe_lore(shift, chance=0.40 if success else 0.15)
    $ lore_hits = [lore_hit] if lore_hit else []

    if success:
        $ notes = [
            "The yard looks normal again, which is the strangest part.",
            "You swear you saw a straight line in the dirt that shouldn't exist.",
        ]
    else:
        $ notes = [
            "You leave before dark. The hedges feel relieved.",
        ]

    return {"success": success, "lore_hits": lore_hits, "notes": notes}
