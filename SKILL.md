---
name: dlfetch
description: Interact with the THISDL (稻香湖学校) learning platform. Submit assignments, check tasks, view schedules, GPA, and manage schoolwork via CLI.
---

Use this skill whenever the user needs to interact with the THISDL school platform (thisdlstu.schoolis.cn). The `dlfetch` CLI source is bundled in this skill directory.

## Setup (first time)

If dlfetch is not yet installed, run:

```bash
bash SKILL_DIR/install.sh
```

This creates a venv, installs dependencies, and adds a `dlfetch` alias to `~/.zshrc`.

Credentials are read from environment variables. Set them before running dlfetch:

```bash
export THISDL_USERNAME="<username>"
export THISDL_PASSWORD="<password>"
```

Alternatively, if the binary is already installed at `~/.local/bin/dlfetch`, use it directly.

## Running dlfetch from source (if binary not built)

```bash
SKILL_DIR/venv/bin/python SKILL_DIR/main.py <command...>
```

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
- When running from source, replace `SKILL_DIR` with the actual skill installation path (e.g., `~/.agents/skills/dlfetch`).
