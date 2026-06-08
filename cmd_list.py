import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, CYAN


def cmd_list(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    subjects = requests.get(
        f"https://thisdlstu.schoolis.cn/api/LearningTask/GetStuSubjectListForSelect?semesterId={semester_id}",
        headers=headers, cookies=cookies
    ).json()["data"]

    print(f"\n📚 {BLUE}Subjects{RESET} — {current_semester['name']}")
    print(f"{'─' * 60}")
    print(f"  {'ID':<8} {'Code':<8} {'Subject'}")
    print(f"  {'─' * 56}")
    for s in subjects:
        name = s["eName"] or s["name"]
        print(f"  {CYAN}{s['id']:<8}{RESET} {s['subjectCode']:<8} {name}")
