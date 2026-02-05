################################################################################
# game/systems/time_and_events.rpy
#
# SYSTEM: TIME + EVENT SCHEDULER
#
# ROLE IN PROJECT:
# - Controls in-world time (days + narrative blocks)
# - Drives delayed story beats
# - Handles "waiting" in a story-friendly way
# - Replaces hardcoded jumps and fake timers
#
# DESIGN PHILOSOPHY:
# - Time is discrete, not continuous
# - Events are condition-based, not scripted chains
# - Nothing runs twice unless explicitly reset
#
# THINK OF THIS AS:
# A narrative clock + a one-shot story trigger engine
################################################################################

###############################################################################
# SECTION 1: TIME STATE (PERSISTENT SAVE DATA)
###############################################################################
#
# These variables are saved automatically.
# They define the "current moment" in the story world.
#
# day:
#   Integer counter. Starts at 1.
#   Use this for pacing long arcs.
#
# time_block:
#   Narrative granularity.
#   Blocks represent meaningful story phases.
#
# Recommended meaning:
#   morning   = fresh actions, new posts, travel
#   afternoon = investigation, jobs, replies
#   night     = reflection, sleep, horror beats
#
###############################################################################

default day = 1
default time_block = "night"   # "morning" | "afternoon" | "night"

###############################################################################
# SECTION 2: EVENT MEMORY
###############################################################################
#
# event_fired:
#   Set of event IDs that already ran.
#   Prevents repeated triggers.
#
# event_queue:
#   List of all scheduled narrative events.
#   Each event is a dict:
#
#   {
#     "id": "unique.id",
#     "condition": function returning bool,
#     "action": function,
#     "desc": optional string
#   }
#
###############################################################################

default event_fired = set()
default event_queue = []

###############################################################################
# SECTION 3: STORY FLAGS (CUSTOMIZE FREELY)
###############################################################################
#
# These are narrative switches.
# They are NOT part of the scheduler itself.
# They exist to feed conditions into it.
#
# Add new flags as the story grows.
# Never delete old ones mid-project.
#
###############################################################################

default first_job_done = False

default replies_batch_1_ready = False
default replies_batch_2_ready = False

default meetup_set = False
default meetup_available = False

###############################################################################
# SECTION 4: CORE TIME ENGINE
###############################################################################
#
# This is the only place that time advances.
# Everything else reacts to it.
#
###############################################################################

init python:

    TIME_BLOCKS = ["morning", "afternoon", "night"]

    def time_index(tb):
        try:
            return TIME_BLOCKS.index(tb)
        except:
            return 0

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

    def sleep_advance():
        """
        Called by beds / sleep actions.
        Advances time and runs due events.
        """
        advance_time_block(1)
        run_due_events()

###############################################################################
# SECTION 5: EVENT QUEUE API
###############################################################################
#
# This is the heart of the scheduler.
#
# Events are:
# - Registered once
# - Checked often
# - Fired once
#
###############################################################################

    def queue_event(event_id, condition_fn, action_fn, description=""):
        """
        Registers a narrative event.

        event_id:
            Unique string identifier.

        condition_fn:
            Function returning True when event should fire.

        action_fn:
            Function that executes story logic.

        description:
            Optional debug label.
        """
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
# SECTION 6: CONDITION HELPERS
###############################################################################
#
# These exist to keep event definitions readable.
# Add more as needed.
#
###############################################################################

    def is_day_at_least(n):
        return store.day >= int(n)

    def is_time(tb):
        return store.time_block == tb

###############################################################################
# SECTION 7: EVENT ACTIONS (STORY EFFECTS)
###############################################################################
#
# These functions mutate story state.
# They are what actually "happen".
#
###############################################################################

    def unlock_replies_batch_1():
        store.replies_batch_1_ready = True
        renpy.notify("New replies arrived.")

    def unlock_replies_batch_2():
        store.replies_batch_2_ready = True
        renpy.notify("More replies arrived.")
        try:
            obj_pin("prog.onboarding.read_replies_mandatory")
        except:
            pass

    def unlock_meetup():
        store.meetup_available = True
        renpy.notify("Meet-up is now available.")

###############################################################################
# SECTION 8: EVENT REGISTRATION
###############################################################################
#
# This is where story logic gets scheduled.
# This is the only section that grows long-term.
#
###############################################################################

    def register_core_events():
        """
        Called once at game start.
        """

        # Partial replies after first job
        queue_event(
            event_id="ev.replies.batch1",
            description="Replies after first job",
            condition_fn=lambda:
                store.first_job_done and
                is_day_at_least(2) and
                not store.replies_batch_1_ready,
            action_fn=unlock_replies_batch_1
        )

        # Mandatory replies later
        queue_event(
            event_id="ev.replies.batch2",
            description="Mandatory replies later",
            condition_fn=lambda:
                store.replies_batch_1_ready and
                is_day_at_least(3) and
                not store.replies_batch_2_ready,
            action_fn=unlock_replies_batch_2
        )

        # Meet-up unlock
        queue_event(
            event_id="ev.meetup.unlock",
            description="Meet-up available",
            condition_fn=lambda:
                store.meetup_set and
                not store.meetup_available,
            action_fn=unlock_meetup
        )

###############################################################################
# SECTION 9: ENTRY POINT LABELS
###############################################################################
#
# These are called by story scripts.
#
###############################################################################

label time_system_begin:
    $ register_core_events()
    return

label sleep_and_process:
    $ sleep_advance()
    return
