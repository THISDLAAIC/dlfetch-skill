---
name: dlfetch
description: Interact with the THISDL (稻香湖学校) learning platform. Submit assignments, check tasks, view schedules, GPA, and manage schoolwork via CLI.
---

Use this skill whenever the user needs to interact with the THISDL school platform (thisdlstu.schoolis.cn). You have access to the `dlfetch` CLI tool for all operations.

## Setup

dlfetch must be installed and configured with credentials:

```bash
export THISDL_USERNAME="<username>"
export THISDL_PASSWORD="<password>"
```

The dlfetch binary is at `~/.local/bin/dlfetch`.

## Commands

### View semester overview
```bash
dlfetch
```

### List all subjects
```bash
dlfetch list
```

### View learning tasks

**All tasks for a subject:**
```bash
dlfetch tasks -s <SUBJECT_CODE>     # e.g., SCE24 for Honors Physics
```

**Unfinished tasks only:**
```bash
dlfetch tasks -p                    # all subjects
dlfetch tasks -s SCE24 -p           # specific subject, unfinished only
```

**Task detail by ID:**
```bash
dlfetch tasks <TASK_ID>
```

### Submit an assignment

```bash
dlfetch submit <TASK_ID> -f <file_path> -m "<remark>"
```

Multiple files can be uploaded at once with `-f file1.pdf -f file2.pdf`.

### View schedule

```bash
dlfetch schedule           # today
dlfetch schedule -t        # tomorrow
dlfetch schedule -w        # this week as timetable
dlfetch schedule -d 2026-06-01  # specific date
```

### View GPA

```bash
dlfetch gpa                # overview
dlfetch gpa -d             # detailed breakdown
dlfetch gpa -s SCE24       # by subject code
```

## Workflow for submitting assignments

1. Find the task: `dlfetch tasks -s <CODE> -p` to see pending tasks
2. Note the task ID (shown in brackets)
3. Submit: `dlfetch submit <ID> -f <file> -m "remark"`

## Common subject codes

| Code  | Subject                    |
|-------|----------------------------|
| SCE24 | Honors Physics I           |
| MAE01 | Honors Pre-Calculus        |
| SCE04 | Highschool Chemistry I     |
| EN203 | Academic English II        |
| CH202 | Chinese Language and Culture II |
| SOE11 | World History: Modern      |
| PES15 | General PE                 |
| STC12 | Academic English Class     |

## Important

- Always use `dlfetch tasks -p` or `dlfetch tasks -s <CODE> -p` to discover task IDs before submitting — never guess task IDs.
- When a submission fails with an upload error, it may be due to a known bug in dlfetch. Check the source at the dlfetch repo and fix if needed.
- Session tokens expire periodically; dlfetch handles re-authentication automatically.
