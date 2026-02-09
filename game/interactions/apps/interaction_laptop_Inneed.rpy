################################################################################
# interaction_laptop_Inneed.rpy
# InNeed app (background skin + overlay UI)
################################################################################

# -------------------------
# Background image
# -------------------------
image app_inneed_bg = "images/laptop/inneed_screen.png" 

# -------------------------
# State
# -------------------------
default inneed_query = "odd jobs"
default inneed_where = "nowhere"
default inneed_sort = "date"     # "date" or "salary"
default inneed_results = []
default inneed_selected = None
default inneed_mode = "feed"     # "feed" or "detail"

# Job state hooks
default inneed_has_active_job = False
default inneed_active_job_id = None


# -------------------------
# Logic
# -------------------------
init python:

    def inneed_seed_results():
        # Populate results when Find Jobs is clicked
        s = renpy.store
        s.inneed_results = [
            {"id": "job_dogwalk_01", "title": "Dog walk, 30 min", "pay": 25, "where": "Ghoulridge Apts", "posted": "Today"},
            {"id": "job_delivery_01", "title": "Drop off a package", "pay": 40, "where": "Downtown", "posted": "1d ago"},
            {"id": "job_houseclean_01", "title": "Quick clean, 2 rooms", "pay": 75, "where": "Riverside", "posted": "3d ago"},
        ]

    def inneed_accept(job_id):
        s = renpy.store

        if s.inneed_has_active_job:
            return

        s.inneed_has_active_job = True
        s.inneed_active_job_id = job_id


# -------------------------
# Main Screen
# -------------------------
screen laptop_inneed_interactions():
    zorder 200

    # Background skin
    add "app_inneed_bg" xpos 0.15 ypos 0.15


    # Find jobs button
    button:
        xpos 1120 ypos 250
        xsize 310 ysize 85
        background None
        action [
            Function(inneed_seed_results),
            SetVariable("inneed_mode","feed"),
            SetVariable("inneed_selected", None),
        ]

    # Sort: Date posted
    button:
        xpos 420 ypos 345
        xsize 260 ysize 60
        background None
        action SetVariable("inneed_sort","date")

    # Sort: Salary estimate
    button:
        xpos 760 ypos 345
        xsize 320 ysize 60
        background None
        action SetVariable("inneed_sort","salary")

    # Sidebar: Home
    button:
        xpos 55 ypos 700
        xsize 240 ysize 70
        background None
        action [
            SetVariable("laptop_page","home"),
            SetVariable("inneed_mode","feed"),
            SetVariable("inneed_selected", None),
        ]

    # Sidebar: Profile (placeholder)
    button:
        xpos 55 ypos 785
        xsize 240 ysize 70
        background None
        action NullAction()

    # Fake search text
    text "[inneed_query]":
        xpos 360 ypos 266
        size 34
        color "#1b1b1b"

    text "[inneed_where]":
        xpos 820 ypos 266
        size 34
        color "#1b1b1b"

    # Content
    if inneed_mode == "feed":
        use inneed_results_list
    else:
        use inneed_job_detail


# -------------------------
# Results List
# -------------------------
screen inneed_results_list():

    viewport:
        xpos 320 ypos 420
        xsize 1080 ysize 420
        mousewheel True
        draggable True

        vbox:
            spacing 18

            if not inneed_results:
                text "No results yet. Click Find jobs." size 34 color "#2a2a2a"
            else:
                for j in inneed_results:
                    button:
                        xsize 1060
                        ysize 70
                        background None
                        action [
                            SetVariable("inneed_selected", j),
                            SetVariable("inneed_mode", "detail"),
                        ]

                        text "[j['title']]  |  $[j['pay']]  |  [j['where']]  |  [j['posted']]":
                            xpos 10 ypos 15
                            size 30
                            color "#2a2a2a"


# -------------------------
# Job Detail
# -------------------------
screen inneed_job_detail():

    if not inneed_selected:
        text "No job selected." xpos 350 ypos 430 size 34 color "#2a2a2a"
    else:

        frame:
            xpos 320 ypos 420
            xsize 1080 ysize 420
            background Solid((245, 220, 160, 235))
            padding (30, 25)

            vbox:
                spacing 14
                text "[inneed_selected['title']]" size 40 color "#1f1f1f"
                text "Pay: $[inneed_selected['pay']]" size 30 color "#1f1f1f"
                text "Location: [inneed_selected['where']]" size 30 color "#1f1f1f"
                text "Posted: [inneed_selected['posted']]" size 30 color "#1f1f1f"

                null height 10

                hbox:
                    spacing 20

                    textbutton "Back":
                        action [
                            SetVariable("inneed_mode","feed"),
                            SetVariable("inneed_selected", None),
                        ]

                    if not inneed_has_active_job:
                        textbutton "Accept":
                            action [
                                Function(inneed_accept, inneed_selected["id"]),
                                SetVariable("inneed_mode","feed"),
                                SetVariable("inneed_selected", None),
                            ]
                    else:
                        text "Active job already accepted." size 26 color "#1f1f1f"
