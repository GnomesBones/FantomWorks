################################################################################
# interaction_laptop_Schedule.rpy
################################################################################

# Pick ONE:
image app_schedule_bg = "images/laptop/schedule_screen.png"

# image app_schedule_bg = "laptop_schedule_screen.png"

default sched_day = 1
default sched_timeblock = "morning"

init python:
    def sched_advance():
        s = renpy.store
        order = ["morning","afternoon","night"]
        i = order.index(s.sched_timeblock)
        if i < 2:
            s.sched_timeblock = order[i+1]
        else:
            s.sched_timeblock = "morning"
            s.sched_day += 1

screen laptop_schedule_interactions():

    add "app_schedule_bg"

    # Home button (you can map this to your laptop UI instead if needed)
    button:
        xpos 1320 ypos 70
        xsize 140 ysize 60
        background None
        action SetVariable("laptop_page","home")

    # Overlay a little status label (optional)
    text "Day [sched_day] | [sched_timeblock]":
        xpos 90 ypos 90
        size 36
        color "#2a2a2a"

    # Example: show accepted job in the bottom list area
    if inneed_has_active_job and inneed_active_job_id:
        text "InNeed: [inneed_active_job_id]":
            xpos 330 ypos 690
            size 34
            color "#2a2a2a"

    # Temporary debug buttons as invisible click zones
    # Put these somewhere that doesn't break
