# jobs/job_creative.rpy
# Independent creative or contract services: poster builder
# This is a RenPyDraw-friendly placeholder. Swap the builder with your RenPyDraw screen later.

init -2 python:
    def eval_poster(shift, mg):
        reqs = shift.get("requirements", [])
        placed = mg.get("placed", [])
        placed_parts = {p.get("part") for p in placed}
        score = 0
        notes = []

        # Very simple scoring that you can replace with your own logic.
        for r in reqs:
            if "include:" in r:
                need = r.split("include:", 1)[1].strip()
                if need in placed_parts:
                    score += 2
                else:
                    notes.append("Missing required element: %s" % need)

        if mg.get("bg"):
            score += 1

        if len(placed) >= 2:
            score += 1

        success = score >= 3 if reqs else True
        return success, score, notes

label job_creative_play(job_state):
    $ shift = job_state["shift"]
    $ mg = renpy.call_screen("mg_poster_builder", job_state=job_state)

    $ success, score, eval_notes = eval_poster(shift, mg)

    $ lore_hit = maybe_lore(shift, chance=0.40 if success else 0.10)
    $ lore_hits = [lore_hit] if lore_hit else []

    if success:
        $ notes = [
            "The client nods like you accidentally matched something they remember from childhood.",
            "Your design prints with a faint watermark you did not add.",
            "Score: %d" % score,
        ] + eval_notes
    else:
        $ notes = [
            "The client pauses, then asks if you can 'make it look more like the old one.'",
            "Score: %d" % score,
        ] + eval_notes

    return {"success": success, "lore_hits": lore_hits, "notes": notes}
