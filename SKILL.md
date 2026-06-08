---
name: dlfetch
description: Interact with the THISDL (稻香湖学校) learning platform. Submit assignments, check tasks, view schedules, GPA, and manage schoolwork via CLI.
---

Use this skill whenever the user needs to interact with the THISDL school platform (thisdlstu.schoolis.cn).

## Setup (first time)

If the `dlfetch` command is not available, install from the skill directory:

```bash
bash /path/to/skill/install.sh
```

This creates a venv, installs dependencies, and sets up a `dlfetch` alias. Credentials are read from `THISDL_USERNAME` and `THISDL_PASSWORD` environment variables.

If dlfetch is already installed (binary in PATH or alias), skip this step.

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
dlfetch tasks -s <SUBJECT_CODE>
```

**Unfinished tasks only:**
```bash
dlfetch tasks -p
dlfetch tasks -s SCE24 -p
```

**Task detail by ID:**
```bash
dlfetch tasks <TASK_ID>
```

### Submit an assignment

```bash
dlfetch submit <TASK_ID> -f <file_path> -m "<remark>"
```

Multiple files: `-f file1.pdf -f file2.pdf`

### View schedule

```bash
dlfetch schedule
dlfetch schedule -t        # tomorrow
dlfetch schedule -w        # this week
dlfetch schedule -d 2026-06-01
```

### View GPA

```bash
dlfetch gpa
dlfetch gpa -d             # detailed breakdown
dlfetch gpa -s SCE24       # by subject code
```

## Workflow for submitting assignments

1. Find the task: `dlfetch tasks -s <CODE> -p`
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

- Always use `dlfetch tasks -p` or `dlfetch tasks -s <CODE> -p` to discover task IDs — never guess.
- Session tokens expire periodically; dlfetch handles re-authentication automatically.

