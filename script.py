import os
import random
import subprocess
from datetime import datetime, timedelta

# الملف اللي غادي نعملو عليه commits
FILE_PATH = "info.txt"

# دالة لتشغيل أوامر git
def run(cmd, env=None):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, env=env)

# دالة لإنشاء commit بتاريخ محدد
def git_commit(message, commit_date):
    # نضيف الملف
    run(["git", "add", FILE_PATH])

    # env مع تاريخ commit
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_date.isoformat()
    env["GIT_COMMITTER_DATE"] = commit_date.isoformat()

    # commit
    run([
        "git", "commit",
        "-m", message,
        "--date", commit_date.isoformat()
    ], env=env)

# push commits
def git_push():
    run(["git", "push"])

# توليد وقت عشوائي فاليوم
def random_time(date):
    hour = random.randint(9, 21)      # بين 9 صباحا و 9 مساء
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return date.replace(hour=hour, minute=minute, second=second)

# الدالة الرئيسية لتوليد commits
def fake_commits(
    start_date,
    end_date,
    min_commits=1,
    max_commits=3,
    skip_weekends=True,
    skip_chance=0.3
):
    current = start_date

    while current <= end_date:

        # skip weekends
        if skip_weekends and current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        # skip randomly
        if random.random() < skip_chance:
            current += timedelta(days=1)
            continue

        # عدد commits اليوم
        commits_today = random.randint(min_commits, max_commits)

        for i in range(commits_today):
            commit_time = random_time(current)

            message = random.choice([
                "update",
                "small fix",
                "minor improvement",
                "refactor",
                "cleanup",
                "progress update"
            ])

            # نكتب فالملف info.txt
            with open(FILE_PATH, "w") as f:
                f.write(f"{message} - {commit_time}")

            # commit
            git_commit(message, commit_time)

        current += timedelta(days=1)

    # push كلشي
    # push كلشي مع set-upstream إذا ما كانش
def git_push():
    # تحقق إذا الفرع مرتبط
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], capture_output=True, text=True)
    if result.returncode != 0:
        # set upstream
        run(["git", "push", "--set-upstream", "origin", "main"])
    else:
        run(["git", "push"])

# ======================
# 🔽 بدّل التواريخ باش تعمّر graph
# سنة كاملة 2024
start_date = datetime(2024, 1, 1)
end_date   = datetime(2024, 12, 31)

# min/max commits لكل نهار
min_commits = 1
max_commits = 3

# تشغيل الدالة
fake_commits(
    start_date,
    end_date,
    min_commits=min_commits,
    max_commits=max_commits,
    skip_weekends=True,
    skip_chance=0.35
)