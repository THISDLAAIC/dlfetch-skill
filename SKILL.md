---
name: dlfetch
description: Interact with the THISDL (稻香湖学校) learning platform. Submit assignments, check tasks, view schedules, GPA, and manage schoolwork via CLI.
---

Use this skill whenever the user needs to interact with the THISDL school platform (thisdlstu.schoolis.cn).

## How to run dlfetch

Try these in order — use the first one that exists:

1. **Binary on PATH** (personal Mac): `~/.local/bin/dlfetch` (just `dlfetch`).
2. **From source** (e.g. school computers, where binaries cannot be executed without admin rights): `~/dlfetch/.venv/bin/python ~/dlfetch/main.py <command...>` — this is what the `dlfetch` alias in `~/.zshrc` points to (the alias only works in interactive shells, so call the venv python directly).
3. **Not installed yet**: install from source — no admin rights needed:
   ```bash
   zsh <(curl -fsSL https://raw.githubusercontent.com/huangdihd/dlfetch/master/install.sh)
   ```
   This clones the repo to `~/dlfetch`, creates a venv, installs dependencies, and adds a `dlfetch` alias to `~/.zshrc`. Then run it via method 2.

There is no source code in this skill directory; the development repo lives at `~/PycharmProjects/THISDLMenu` (on the personal Mac only — rebuild the binary there with `.venv/bin/pyinstaller dlfetch.spec --noconfirm` after code changes).

## Credentials

Credentials are stored in the system keyring (macOS Keychain, service `dlfetch`) — no environment variables needed. Session tokens expire periodically; dlfetch re-authenticates automatically.

- If no credentials are saved yet, `dlfetch` prompts interactively for username and password — this will hang a non-interactive shell. If that happens, ask the user to run `dlfetch` once in their own terminal.
- `dlfetch logout` removes saved credentials and the session (use after a password change or to switch accounts).

## Commands

```bash
dlfetch                    # Neofetch-style semester overview (default)
dlfetch list               # List all subjects with codes and IDs
dlfetch tasks              # Recent tasks with scores and deadlines
dlfetch tasks <TASK_ID>    # Detail for one task
dlfetch tasks -p           # Only unfinished tasks
dlfetch tasks -s SCE24 -p  # Unfinished tasks for one subject
dlfetch tasks -l 20        # Fetch last 20 tasks
dlfetch submit <TASK_ID> -f <file> [-f <file2> ...] [-m "remark"]
dlfetch schedule           # Today's schedule
dlfetch schedule -t        # Tomorrow
dlfetch schedule -w        # This week as a timetable grid
dlfetch schedule -d 2026-06-01
dlfetch gpa                # Current semester GPA
dlfetch gpa -S list        # List all available semesters
dlfetch gpa -S '<name>'    # GPA for a specific semester (e.g. "2025-2026学年 第1学期")
dlfetch gpa -d             # Detailed breakdown per subject
dlfetch gpa -s MAE01 SCE24 # Detail by subject code(s)
dlfetch gpa -i 189741      # Detail by subject ID
dlfetch logout             # Remove saved credentials and session
```

## Semester GPA

Use `-S` (capital S) to switch semesters:

- `dlfetch gpa -S list` — show available semester names  
- `dlfetch gpa -S '2025-2026学年 第1学期'` — GPA for a past semester  
- Without `-S` — current semester (default behavior)

Note: `-S` requires the exact semester name. The `-d`, `-s`, and `-i` flags work with any semester.

## Workflow for submitting assignments

1. Find the task: `dlfetch tasks -s <CODE> -p`
2. Note the task ID (shown in brackets) — never guess task IDs
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
