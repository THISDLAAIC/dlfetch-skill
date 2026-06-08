#! python3
# -*- coding: utf-8 -*-
import argparse

from cmd_info import cmd_info
from cmd_tasks import cmd_tasks, cmd_submit
from cmd_schedule import cmd_schedule
from cmd_gpa import cmd_gpa
from cmd_list import cmd_list

EPILOG = """\
examples:
  dlfetch                  Default neofetch-style overview
  dlfetch tasks            Show all recent tasks with scores
  dlfetch tasks 2273775    Show detail for a specific task by ID
  dlfetch tasks -p         Show only unfinished tasks
  dlfetch tasks -s EN203   Filter tasks by subject code
  dlfetch tasks -l 20      Fetch the last 20 tasks
  dlfetch submit 2259391 -f homework.pdf -m "done"
                           Upload and submit a task
  dlfetch schedule         Show today's schedule
  dlfetch schedule -t      Show tomorrow's schedule
  dlfetch schedule -w      Show this week as a timetable
  dlfetch schedule -d 2026-06-01
                           Show schedule for a specific date
  dlfetch gpa              Show current semester GPA
  dlfetch gpa -d           Show GPA with detailed breakdown per subject
  dlfetch list             List all subjects with their codes and IDs
  dlfetch gpa -s MAE01     Show detail by subject code
  dlfetch gpa -s MAE01 SCE24
                           Show detail for multiple subjects by code
  dlfetch gpa -i 189741    Show detail by subject ID
"""


def main():
    parser = argparse.ArgumentParser(
        prog="dlfetch",
        description="🐱 A neofetch-style CLI for THISDL students",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", metavar="")

    sub.add_parser("info", help="Neofetch-style semester overview (default)")
    sub.add_parser("list", help="List all subjects with their codes and IDs")

    p_tasks = sub.add_parser("tasks", help="List learning tasks with scores and deadlines")
    p_tasks.add_argument("task_id", nargs="?", type=int, help="Show detail for a specific task by ID")
    p_tasks.add_argument("-p", "--pending", action="store_true", help="Show only unfinished tasks")
    p_tasks.add_argument("-l", "--limit", type=int, metavar="N", help="Max number of tasks to fetch (default: 50)")
    p_tasks.add_argument("-s", "--subject", type=str, dest="subject_code", metavar="CODE",
                         help="Filter tasks by subject code, e.g. EN203")

    p_submit = sub.add_parser("submit", help="Upload files and submit a task")
    p_submit.add_argument("task_id", type=int, help="Task ID to submit")
    p_submit.add_argument("-f", "--file", type=str, nargs="+", dest="submit_files", metavar="FILE",
                          help="File(s) to upload and attach")
    p_submit.add_argument("-m", "--remark", type=str, help="Remark/comment for the submission")

    p_sched = sub.add_parser("schedule", help="View daily or weekly class schedule")
    date_group = p_sched.add_mutually_exclusive_group()
    date_group.add_argument("-t", "--tomorrow", action="store_true", help="Show tomorrow's schedule")
    date_group.add_argument("-w", "--week", action="store_true", help="Show this week as a timetable grid")
    date_group.add_argument("-d", "--date", type=str, metavar="YYYY-MM-DD", help="Show schedule for a specific date")

    p_gpa = sub.add_parser("gpa", help="Show current semester GPA")
    p_gpa.add_argument("-d", "--detail", action="store_true", help="Show detailed breakdown per subject")
    p_gpa.add_argument("-s", "--subject", type=str, nargs="+", dest="subject_codes", metavar="CODE",
                       help="Show detail for subject code(s), e.g. MAE01 SCE24")
    p_gpa.add_argument("-i", "--id", type=int, nargs="+", dest="subject_ids", metavar="ID",
                       help="Show detail for subject ID(s) (use 'list' to see IDs)")

    args = parser.parse_args()

    commands = {
        "info": cmd_info,
        "tasks": cmd_tasks,
        "schedule": cmd_schedule,
        "gpa": cmd_gpa,
        "list": cmd_list,
        "submit": cmd_submit,
    }

    if args.command:
        commands[args.command](args)
    else:
        cmd_info(args)


if __name__ == "__main__":
    main()
