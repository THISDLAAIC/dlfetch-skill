import datetime

import requests

from session import get_session, get_current_semester
from constants import logo, headers
from utils import parse_date_string, get_info_lines


def cmd_info(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    tasks = requests.get(
        f"https://thisdlstu.schoolis.cn/api/LearningTask/GetList?semesterId={semester_id}&pageIndex=1&pageSize=12",
        headers=headers, cookies=cookies
    ).json()["data"]["list"]
    unfinished = [t for t in tasks if not t["finishState"]]

    realtime_GPA = requests.get(
        f"https://thisdlstu.schoolis.cn/api/DynamicScore/GetGpa?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    schedule = requests.post(
        "https://rs.api.thisdlit.com/high_school",
        headers=headers, cookies=cookies,
        json={"beginTime": str(datetime.date.today()), "endTime": str(datetime.date.today())}
    ).json()["data"]

    future_lessons = sorted(
        [l for l in schedule if parse_date_string(l["beginTime"]) >= datetime.datetime.now(tz=parse_date_string(l["beginTime"]).tzinfo)],
        key=lambda l: parse_date_string(l["beginTime"])
    )
    next_lesson = future_lessons[0] if future_lessons else None

    info_lines = get_info_lines(current_semester, unfinished, next_lesson, realtime_GPA, semester_id)
    max_lines = max(len(logo), len(info_lines))
    for i in range(max_lines):
        left = logo[i] if i < len(logo) else " " * 9
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<10}  {right}")
