import os
from sys import exit

import requests

from SignIn import sign_in
from constants import headers

session_path = os.path.expanduser("~/.dlfetch_session")


def get_session():
    print("Loading session...")
    session_id = None
    if os.path.exists(session_path):
        with open(session_path) as session_file:
            session_id = session_file.read()

    if session_id:
        test = requests.get(
            "https://thisdlstu.schoolis.cn/api/School/GetSchoolSemesters",
            headers=headers,
            cookies={"SessionId": session_id}
        ).json().get("data")
        if not test:
            session_id = None

    if not session_id:
        print("session_id is empty or expired! Trying to sign in...")
        session_id = sign_in()
        with open(session_path, 'w') as session_file:
            session_file.write(session_id)

    if not session_id:
        print("Login failed.")
        exit(1)

    return session_id


def get_current_semester(cookies):
    semesters = requests.get(
        "https://thisdlstu.schoolis.cn/api/School/GetSchoolSemesters",
        headers=headers,
        cookies=cookies
    ).json().get("data")
    return next(s for s in semesters if s["isNow"])
