import datetime
import re

from constants import BLUE, RESET, GREEN, YELLOW, CYAN


def parse_date_string(date_str):
    match = re.search(r'/Date\((\d+)([+-]\d{4})?\)/', date_str)
    if not match:
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', date_str)
        if not match:
            return None
        year, month, day, hour, minute, second = map(int, match.groups())
        return datetime.datetime(year, month, day, hour, minute, second)
    timestamp_ms = int(match.group(1))
    tz_str = match.group(2) or '+0000'
    sign = 1 if tz_str[0] == '+' else -1
    hours = int(tz_str[1:3])
    minutes = int(tz_str[3:5])
    tz_offset = datetime.timedelta(hours=sign * hours, minutes=sign * minutes)
    tzinfo = datetime.timezone(tz_offset)
    dt_utc = datetime.datetime.fromtimestamp(timestamp_ms / 1000, tz=datetime.timezone.utc)
    return dt_utc.astimezone(tzinfo)

def get_info_lines(current_semester, unfinished, next_lesson, realtime_GPA, current_semester_id):
    # 📋 右侧信息内容
    info_lines = [
        f"🏫  {BLUE}THISDL Student Info{RESET}",
        f"{'-' * 28}",
        f"Semester  : {current_semester['name']} ({current_semester_id})",
        f"GPA       : {GREEN}{realtime_GPA}{RESET}",
        f"Tasks     : {YELLOW}{len(unfinished)} not handed in(in last 12 tasks){RESET}",
        f"Next Class: {CYAN}{next_lesson['classInfo']['className']} in {next_lesson['playgroundName']}{RESET}" if next_lesson else f"Next Class: {CYAN}None today{RESET}"
    ]
    return info_lines