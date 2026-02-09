################################################################################
# game/systems/time_and_events.rpy
#
# SYSTEM: TIME + EVENT SCHEDULER + ACTIVITY POINTS
#
# INTEGRATES WITH:
# - game/core/game_state.rpy  (replies + shared app flags)
# - game/systems/objectives.rpy (sleep gating + objective completion)
#
# DESIGN:
# - Time is discrete: morning, afternoon, night
# - A "tick" is one time block
# - Activity Points (AP) push time forward when threshold is reached
# - When time changes:
#     - process reply arrivals (from game_state.rpy)
#     - run due narrative events (event_queue)
################################################################################

###############################################################################
# SECTION 1: TIME STATE (PERSISTENT SAVE DATA)
###############################################################################

default day = 1
default time_block = "night"   # "morning" | "afternoon" | "night"

###############################################################################
# SECTION 2: ACTIVITY POINT SYSTEM (PERSISTENT SAVE DATA)
###############################################################################
# Use spend_ap(cost) for actions like:
# - travel, investigate, job tasks, social, studying
#
# When ap_current reaches ap_threshold_per_block, time advances 1 block.
###############################################################################

default ap_current = 0
default ap_threshold_per_block = 4

default minutes_into_block = 0
default minutes_per_ap = 15


###############################################################################
# SECTION 3: EVENT MEMORY (PERSISTENT SAVE DATA)
###############################################################################

default event_fired = set()
default event_queue = []

###############################################################################
# SECTION 4: STORY FLAGS (CUSTOMIZE FREELY)
###############################################################################
# Keep long-term story flags here.
# Do NOT duplicate app progression flags that live in core/game_state.rpy.
###############################################################################

default meetup_set = False
default meetup_available = False

###############################################################################
# SECTION 5: CORE TIME ENGINE
###############################################################################

init python:

    TIME_BLOCKS = ["morning", "afternoon", "night"]

    def time_index(tb):
        try:
            return TIME_BLOCKS.index(tb)
        except:
            return 0

    def current_tick():
        """
        Converts (day, time_block) into a single integer tick.

        tick 0 = day 1 morning
        tick 1 = day 1 afternoon
        tick 2 = day 1 night
        tick 3 = day 2 morning
        """
        return ((int(store.day) - 1) * len(TIME_BLOCKS)) + time_index(store.time_block)

    def set_time_from_tick(tick):
        """
        Converts a tick back into (day, time_block).
        """
        tick = int(tick)
        blocks = len(TIME_BLOCKS)

        if tick < 0:
            tick = 0

        store.day = (tick // blocks) + 1
        store.time_block = TIME_BLOCKS[tick % blocks]

    def after_time_change():
        """
        Single place to react whenever time changes.
        - Process reply arrivals (game_state.rpy)
        - Run due narrative events (event_queue)
        - Reset AP for the new block
        - Auto-advance objective steps that depend on time/replies
        """
        # Replies arriving (from core/game_state.rpy)
        try:
            process_reply_arrivals(current_tick())
        except Exception as ex:
            renpy.log("Reply arrival processing error: %r" % ex)

        # Fire scheduled narrative events
        try:
            run_due_events()
        except Exception as ex:
            renpy.log("Event processing error: %r" % ex)

        # Reset AP for the new time block (recommended)
        store.ap_current = 0
        store.minutes_into_block = 0

        # Objective hooks (optional but useful for your onboarding flow)
        # Auto-complete "wait for replies" when any reply arrives
        try:
            if getattr(store, "pinned_step_id", None) == "prog.onboarding.wait_replies_1":
                if any([r.arrived for r in store.replies]):
                    obj_complete(None)
        except Exception as ex:
            renpy.log("Objective hook wait_replies_1 error: %r" % ex)

        # Auto-complete "read replies mandatory" when all mandatory are read
        try:
            if getattr(store, "pinned_step_id", None) == "prog.onboarding.read_replies_mandatory":
                if all_mandatory_read():
                    obj_complete(None)
        except Exception as ex:
            renpy.log("Objective hook read_replies_mandatory error: %r" % ex)

    def advance_time_block(steps=1):
        """
        Moves time forward by N blocks.
        Wraps automatically into next day.
        """
        i = time_index(store.time_block)

        for _ in range(int(steps)):
            i += 1
            if i >= len(TIME_BLOCKS):
                i = 0
                store.day += 1

        store.time_block = TIME_BLOCKS[i]

        after_time_change()

    def sleep_advance():
        """
        Called by bed / sleep actions.
        Default behavior: advance by 1 block.
        """
        advance_time_block(1)

###############################################################################
# SECTION 6: ACTIVITY POINT API
###############################################################################
# Call spend_ap(cost) after actions.
# If threshold reached, time advances automatically.
###############################################################################

init python:

    def spend_ap(cost=1):
        """
        Adds AP and advances time when threshold is reached.
        Returns True if time advanced at least once.
        """
        cost = int(cost)
        if cost < 0:
            cost = 0

        store.ap_current += cost
        store.minutes_into_block += cost * int(store.minutes_per_ap)

        advanced = False
        while store.ap_current >= int(store.ap_threshold_per_block):
            store.ap_current -= int(store.ap_threshold_per_block)
            advance_time_block(1)
            advanced = True

        return advanced

###############################################################################
# SECTION 7: EVENT QUEUE API
###############################################################################
# Heart of the scheduler. Events fire once.
###############################################################################

init python:

    def queue_event(event_id, condition_fn, action_fn, description=""):
        store.event_queue.append({
            "id": event_id,
            "condition": condition_fn,
            "action": action_fn,
            "desc": description,
        })

    def has_fired(event_id):
        return event_id in store.event_fired

    def mark_fired(event_id):
        store.event_fired.add(event_id)

    def run_due_events():
        """
        Scans the queue and fires all valid events.
        Safe to call often.
        """
        for e in list(store.event_queue):
            eid = e.get("id")

            if not eid or has_fired(eid):
                continue

            try:
                if e["condition"]():
                    e["action"]()
                    mark_fired(eid)
            except Exception as ex:
                renpy.log("Event error %s: %r" % (eid, ex))

        renpy.restart_interaction()

###############################################################################
# SECTION 8: CONDITION HELPERS
###############################################################################

init python:

    def is_day_at_least(n):
        return store.day >= int(n)

    def is_time(tb):
        return store.time_block == tb

    def block_start_hour(tb):
        return {
            "morning": 8,
            "afternoon": 14,
            "night": 20,
        }.get(tb, 0)

    def clock_time():
        h = block_start_hour(store.time_block)
        m = int(store.minutes_into_block)

        h = (h + (m // 60)) % 24
        m = m % 60

        return f"{h:02}:{m:02}"


###############################################################################
# SECTION 9: EVENT ACTIONS (STORY EFFECTS)
###############################################################################

init python:

    def unlock_meetup():
        store.meetup_available = True
        renpy.notify("Meet-up is now available.")

###############################################################################
# SECTION 10: EVENT REGISTRATION
###############################################################################
# Keep this for long-term scheduled story beats.
# Replies are scheduled by your app logic and arrive via game_state.rpy.
###############################################################################

init python:

    # Condition functions must be top-level (pickle-safe + visible here).
    def cond_meetup_unlock():
        return store.meetup_set and (not store.meetup_available)

    def register_core_events():
        """
        Called once at game start.
        """
        queue_event(
            event_id="ev.meetup.unlock",
            condition_fn=cond_meetup_unlock,
            action_fn=unlock_meetup,
            description="Meet-up available",
        )

###############################################################################
# SECTION 11: ENTRY POINT LABELS
###############################################################################

label time_system_begin:
    $ register_core_events()

    # Ensure replies exist so inbox is stable even before anything arrives
    $ ensure_default_replies_exist()

    # Process anything due right now
    $ process_reply_arrivals(current_tick())
    return

label sleep_and_process:

    # Hard gate sleep behind your objective system.
    # This prevents bed clipping.
    if not obj_can_sleep():
        "Not yet."
        return

    # Complete the currently pinned sleep step (sleep_1, sleep_2, etc.)
    $ obj_complete(None)

    # Advance time by one block and process arrivals and events
    $ sleep_advance()
    return
