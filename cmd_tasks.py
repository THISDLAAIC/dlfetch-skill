import os

import requests

from session import get_session, get_current_semester
from constants import headers, BLUE, RESET, GREEN, YELLOW, CYAN
from utils import parse_date_string


def upload_file(file_path, cookies):
    if not os.path.exists(file_path):
        print(f"  File not found: {file_path}")
        return None

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".zip": "application/zip",
        ".txt": "text/plain",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }
    content_type = mime_types.get(ext, "application/octet-stream")
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f:
        r = requests.post(
            "https://thisdlstu.schoolis.cn/api/LearningTask/UploadDocument",
            headers={"User-Agent": "DLFetch"},
            cookies=cookies,
            files={"fileBase": (filename, f, content_type)}
        )

    data = r.json()
    if data["state"] != 0:
        print(f"  Upload failed: {data.get('msgCN') or data.get('msg')}")
        return None

    doc = data["data"]
    print(f"  Uploaded: {GREEN}{filename}{RESET} ({file_size // 1024}KB)")
    return {
        "id": doc.get("id") or doc.get("fileId"),
        "type": ext,
        "size": file_size,
        "name": filename,
        "url": doc.get("url"),
        "sort": doc.get("sort", 0),
        "finaltype": doc.get("finaltype", ext.lstrip(".")),
    }


def cmd_submit(args):
    cookies = {"SessionId": get_session()}

    if not args.submit_files and not args.remark:
        print("  Use: dlfetch submit <ID> -f <file> [-m remark]")
        return

    task_id = args.task_id
    print(f"\n📤 {BLUE}Submitting task {task_id}{RESET}")
    print(f"{'─' * 40}")

    uploaded_docs = []
    if args.submit_files:
        for fp in args.submit_files:
            doc = upload_file(fp, cookies)
            if doc:
                uploaded_docs.append(doc)
            else:
                print(f"  Skipping failed upload: {fp}")

    payload = {
        "learningTaskId": task_id,
        "remark": args.remark or "",
        "learningTaskStudentDocuments": uploaded_docs,
    }

    r = requests.post(
        "https://thisdlstu.schoolis.cn/api/LearningTask/Save",
        headers={**headers, "Content-Type": "application/json"},
        cookies=cookies,
        json=payload,
    ).json()

    if r["state"] == 0:
        print(f"\n  {GREEN}✅ Submitted successfully!{RESET}")
    else:
        print(f"\n  {YELLOW}Submit failed: {r.get('msgCN') or r.get('msg')}{RESET}")


def cmd_tasks(args):
    cookies = {"SessionId": get_session()}
    current_semester = get_current_semester(cookies)
    semester_id = current_semester["id"]

    if args.task_id:
        r = requests.get(
            f"https://thisdlstu.schoolis.cn/api/LearningTask/GetDetail?learningTaskId={args.task_id}",
            headers=headers, cookies=cookies
        ).json()
        if r["state"] != 0:
            print(f"  Task not found or access denied")
            return
        t = r["data"]

        name = t["learningTaskName"]
        subject = t["subjectEName"] or t["subjectName"]
        task_type = t["learningTaskTypeEName"] or t["learningTaskTypeName"]
        score = t.get("score")
        total = t.get("totalScore")
        class_avg = t.get("classAvgScore")
        class_max = t.get("classMaxScore")
        finished = t["finishState"]
        comment = t.get("comment") or t.get("remark") or ""
        content = t.get("content") or ""
        attachments = t.get("learningTaskDocuments", [])
        eva = t.get("evaProjects", [])

        status = f"{GREEN}Done{RESET}" if finished else f"{YELLOW}Pending{RESET}"

        print(f"\n📄 {BLUE}{name}{RESET}")
        print(f"{'─' * 50}")
        print(f"  Subject   : {subject}")
        print(f"  Type      : {task_type}")
        print(f"  Status    : {status}")

        if score is not None and total:
            print(f"  Score     : {GREEN}{score}{RESET} / {total}")
        if class_avg is not None:
            print(f"  Class Avg : {class_avg}")
        if class_max is not None:
            print(f"  Class Max : {class_max}")

        if eva:
            parts = [f"{e['eName'] or e['name']} ({e['proportion']:.0f}%)" for e in eva]
            print(f"  Category  : {', '.join(parts)}")

        if comment:
            print(f"  Comment   : {comment}")

        if content:
            print(f"  Content   : {content}")

        if attachments:
            print(f"  Attachments:")
            for a in attachments:
                size_kb = a["size"] / 1024
                print(f"    · {a['name']} ({a['type']}, {size_kb:.0f}KB)")
                print(f"      {a['url']}")
        return

    page_size = args.limit if args.limit else 50
    subject_id = None

    if args.subject_code:
        subject_list = requests.get(
            f"https://thisdlstu.schoolis.cn/api/LearningTask/GetStuSubjectListForSelect?semesterId={semester_id}",
            headers=headers, cookies=cookies
        ).json()["data"]
        code_map = {s["subjectCode"].upper(): s["id"] for s in subject_list}
        subject_id = code_map.get(args.subject_code.upper())
        if not subject_id:
            print(f"  Subject code {CYAN}{args.subject_code}{RESET} not found")
            return

    begin = current_semester.get("beginDate", "2026-01-01")[:10]
    end = current_semester.get("endDate", "2026-12-31")[:10]

    params = f"semesterId={semester_id}&pageIndex=1&pageSize={page_size}&beginTime={begin}&endTime={end}&key=&typeId=null&mode=null"
    if subject_id:
        params += f"&subjectId={subject_id}"

    tasks = requests.get(
        f"https://thisdlstu.schoolis.cn/api/LearningTask/GetList?{params}",
        headers=headers, cookies=cookies
    ).json()["data"]["list"]

    if args.pending:
        tasks = [t for t in tasks if not t["finishState"]]

    unfinished = [t for t in tasks if not t["finishState"]]
    finished = [t for t in tasks if t["finishState"]]

    title = f" ({args.subject_code.upper()})" if args.subject_code else ""
    print(f"\n📋 {BLUE}Learning Tasks{RESET}{title} ({current_semester['name']})")
    print(f"{'─' * 40}")

    if finished and not args.pending:
        print(f"{GREEN}✅ Handed in:{RESET}")
        for t in finished:
            score_str = ""
            if t.get('score') is not None and t.get('totalScore'):
                score_str = f" ({t['score']}/{t['totalScore']})"
            print(f"  [{t['id']}] {t['name']}{score_str}")
            if t.get('subjectName') and not subject_id:
                print(f"    Subject: {t['subjectName']}")

    if unfinished:
        print(f"{YELLOW}⏳ Not handed in:{RESET}")
        for t in unfinished:
            print(f"  [{t['id']}] {t['name']}")
            if t.get('subjectName') and not subject_id:
                print(f"    Subject: {t['subjectName']} ({t.get('subjectCode', '')})")
            if t.get('typeName'):
                print(f"    Type: {t['typeName']}")
            if t.get('endTime'):
                end_dt = parse_date_string(t['endTime'])
                if end_dt:
                    print(f"    Deadline: {end_dt.strftime('%Y-%m-%d %H:%M')}")

    print(f"Total: {len(tasks)} | {GREEN}Done: {len(finished)}{RESET} | {YELLOW}Pending: {len(unfinished)}{RESET}")
