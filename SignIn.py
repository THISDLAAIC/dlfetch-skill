import os

from sys import exit
import hashlib
import time
import requests

from constants import headers, errors

def md5_upper(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest().upper()

def password_hash(password: str, timestamp: int):

    first = md5_upper(password)
    final_hash = md5_upper(first + str(timestamp))

    return final_hash

def sign_in() -> str | None:
    user_name = os.environ.get('THISDL_USERNAME')
    password = os.environ.get('THISDL_PASSWORD')

    if not user_name or not password:
        print('Please set environment variables THISDL_USERNAME and THISDL_PASSWORD')
        exit(1)

    timestamp = int(time.time())
    hashed_password = password_hash(password, timestamp)
    try:
        session_id = requests.get(
            "https://thisdlstu.schoolis.cn/api/MemberShip/GetStudentCaptchaForLogin",
            headers=headers
        ).cookies.get('SessionId')
    except ValueError:
        print("Failed to get session id")
        return None

    print("Got session id successfully!")
    print("Trying to login!")

    login_res = requests.post(
        "https://thisdlstu.schoolis.cn/api/MemberShip/Login?captcha=",
        headers=headers,
        cookies={
            "SessionId": session_id,
        },
        json={
            "name": user_name,
            "password": hashed_password,
            "timestamp": timestamp
        }
    )

    try:
        if login_res.json()['data']:
            print("Login successfully!")
            return session_id
        else:
            print(errors.get(login_res.json()['state']))
            return None
    except (ValueError, KeyError):
        print('Unknown error')
        return None


if __name__ == '__main__':
    print(sign_in())