import datetime

import requests

from session import get_session
from constants import headers, BLUE, RESET, GREEN, CYAN
from utils import parse_date_string

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def truncate(s, width):
    if len(s) <= width:
        return s
    return s[:width - 1] + "~"


def print_day_schedule(lessons, target_date, now):
    if not lessons:
        print(f"  No classes!")
        return

    lessons = sorted(lessons, key=lambda l: parse_date_string(l["beginTime"]))

    for l in lessons:
        begin = parse_date_string(l["beginTime"])
        end = parse_date_string(l["endTime"])
        class_name = l.get("classInfo", {}).get("className", "Unknown")
        location = l.get("playgroundName", "")

        if target_date == datetime.date.today():
            if begin and begin < now < end:
                status = f"{GREEN}◀ NOW{RESET}"
            elif end and end < now:
                status = f"  done"
            else:
                status = "      "
        else:
            status = "      "

        time_str = f"{begin.strftime('%H:%M')}-{end.strftime('%H:%M')}" if begin and end else "??:??-??:??"
        loc_str = f" @ {location}" if location else ""
        print(f"  {status}  {time_str}  {CYAN}{class_name}{RESET}{loc_str}")


def cmd_schedule(args):
    cookies = {"SessionId": get_session()}
    now = datetime.datetime.now()

    if args.week:
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        sunday = monday + datetime.timedelta(days=6)

        schedule = requests.post(
            "https://rs.api.thisdlit.com/high_school",
            headers=headers, cookies=cookies,
            json={"beginTime": str(monday), "endTime": str(sunday)}
        ).json()["data"]

        by_day = {}
        for l in schedule:
            d = parse_date_string(l["beginTime"]).date()
            by_day.setdefault(d, []).append(l)

        time_slots = set()
        grid = {}
        for i in range(7):
            d = monday + datetime.timedelta(days=i)
            for l in by_day.get(d, []):
                begin = parse_date_string(l["beginTime"])
                end = parse_date_string(l["endTime"])
                key = (begin.strftime("%H:%M"), end.strftime("%H:%M"))
                time_slots.add(key)
                class_name = l.get("classInfo", {}).get("className", "")
                grid[(key, d)] = class_name

        if not time_slots:
            print(f"\n📅 {BLUE}This Week{RESET} ({monday} ~ {sunday})")
            print(f"{'─' * 50}")
            print("  No classes this week!")
            return

        time_slots = sorted(time_slots)

        day_width = 14
        time_width = 13
        header_days = []
        for i in range(7):
            d = monday + datetime.timedelta(days=i)
            day_name = WEEKDAYS[d.weekday()]
            label = f"{day_name} {d.day}"
            if d == today:
                label += " *"
            header_days.append(f"{label:^{day_width}}")

        print(f"\n📅 {BLUE}This Week{RESET} ({monday} ~ {sunday})")
        print()
        print(f"  {'':>{time_width}}  {'  '.join(header_days)}")
        print(f"  {'─' * (time_width + 2 + (day_width + 2) * 7)}")

        for ts in time_slots:
            time_label = f"{ts[0]}-{ts[1]}"
            cells = []
            for i in range(7):
                d = monday + datetime.timedelta(days=i)
                name = grid.get((ts, d), "")
                is_today = d == today
                cell = truncate(name, day_width)
                if is_today:
                    cell = f"{GREEN}{cell:^{day_width}}{RESET}"
                else:
                    cell = f"{CYAN}{cell:^{day_width}}{RESET}"
                cells.append(cell)
            print(f"  {time_label:>{time_width}}  {'  '.join(cells)}")
    else:
        if getattr(args, 'date', None):
            target_date = datetime.date.fromisoformat(args.date)
        elif getattr(args, 'tomorrow', False):
            target_date = datetime.date.today() + datetime.timedelta(days=1)
        else:
            target_date = datetime.date.today()

        schedule = requests.post(
            "https://rs.api.thisdlit.com/high_school",
            headers=headers, cookies=cookies,
            json={"beginTime": str(target_date), "endTime": str(target_date)}
        ).json()["data"]

        day_label = "Today" if target_date == datetime.date.today() else "Tomorrow" if target_date == datetime.date.today() + datetime.timedelta(days=1) else str(target_date)
        print(f"\n📅 {BLUE}{day_label}'s Schedule{RESET} ({target_date})")
        print(f"{'─' * 40}")
        print_day_schedule(schedule, target_date, now)
