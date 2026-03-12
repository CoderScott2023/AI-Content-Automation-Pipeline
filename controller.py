import subprocess
import time

jobs = [
    {
        "name": "bible",
        "script": "bible_channel.py",
        "folder": r"Youtube-Faceless-Automation-Channel\bible_channel",
        "python": r"Youtube-Faceless-Automation-Channel\bible_channel\.venv\Scripts\python.exe",
        "interval": 43200,
        "offset": 0,
    },
    {
        "name": "finance",
        "script": "finance_channel.py",
        "folder": r"Youtube-Faceless-Automation-Channel\finance_channel",
        "python": r"Youtube-Faceless-Automation-Channel\finance_channel\.venv\Scripts\python.exe",
        "interval": 43200,
        "offset": 3600,
    },
]

last_run = {}

start_time = time.time()

while True:
    now = time.time()

    for job in jobs:
        first_time = start_time + job["offset"]

        if now < first_time:
            continue

        last = last_run.get(job["name"], first_time - job["interval"])

        if now - last >= job["interval"]:
            print(f"Starting {job['script']}")
            subprocess.Popen(
                [job["python"], job["script"]],
                cwd=job["folder"],
            )
            last_run[job["name"]] = now

    time.sleep(60)
