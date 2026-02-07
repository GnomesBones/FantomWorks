

# =====================================================
# GAME STATE
# Shared progression flags across systems + apps
# =====================================================

# -----------------------------
# APP PROGRESSION FLAGS
# -----------------------------

default notreddit_posted = False
default notreddit_post_title = ""
default notreddit_post_body = ""

default first_job_active = False
default first_job_done = False

default replies_mandatory_mode = False


# -----------------------------
# REPLY / MESSAGE SYSTEM
# -----------------------------

default replies = []
default reply_queue = []


init python:

    # -----------------------------
    # Reply Object
    # -----------------------------
    class Reply(object):

        def __init__(self, key, sender, text, mandatory=False):
            self.key = key
            self.sender = sender
            self.text = text
            self.mandatory = mandatory
            self.arrived = False
            self.read = False


    # -----------------------------
    # Safety Init
    # -----------------------------
    def ensure_default_replies_exist():

        keys = [r.key for r in replies]

        if "job_partial" not in keys:
            replies.append(
                Reply(
                    "job_partial",
                    "InNeed",
                    "We received your completion. Reviewing now.",
                    mandatory=False
                )
            )

        if "job_full" not in keys:
            replies.append(
                Reply(
                    "job_full",
                    "InNeed",
                    "Approved. Next steps sent.",
                    mandatory=True
                )
            )


    # -----------------------------
    # Scheduling
    # -----------------------------
    def schedule_reply(key, arrive_time):
        reply_queue.append({
            "key": key,
            "time": int(arrive_time)
        })


    def process_reply_arrivals(current_time):

        for item in list(reply_queue):

            if item["time"] <= current_time:

                for r in replies:
                    if r.key == item["key"]:
                        r.arrived = True

                reply_queue.remove(item)


    # -----------------------------
    # Read Tracking
    # -----------------------------
    def mark_reply_read(key):

        for r in replies:
            if r.key == key:
                r.read = True


    def all_mandatory_read():

        for r in replies:

            if r.mandatory and r.arrived and not r.read:
                return False

        return True


    # -----------------------------
    # FIRST JOB → REPLY SCHEDULING
    # -----------------------------
    def schedule_replies_after_first_job(current_time):

        global replies_mandatory_mode

        ensure_default_replies_exist()

        schedule_reply("job_partial", current_time + 1)
        schedule_reply("job_full", current_time + 3)

        replies_mandatory_mode = True
