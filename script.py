import os
import random
import datetime
import subprocess

STATE_FILE = "state.txt"

COMMITS_MIN = 7
COMMITS_MAX = 12

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r") as f:
        data = f.read().strip().split(",")

    if len(data) != 2:
        return {}

    return {"date": data[0], "count": int(data[1])}

def save_state(date, count):
    with open(STATE_FILE, "w") as f:
        f.write(f"{date},{count}")

def should_run_today():
    return random.random() < (4/7)

def make_commit():
    now = datetime.datetime.now().isoformat()

    with open("log.txt", "a") as f:
        f.write(now + "\n")

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"update {now}"])

def main():
    today = str(datetime.date.today())
    state = load_state()

    # reset daily counter
    if state.get("date") != today:
        if not should_run_today():
            save_state(today, 0)
            print("Skipping today")
            return

        target = random.randint(COMMITS_MIN, COMMITS_MAX)
        save_state(today, 0)
    else:
        target = COMMITS_MAX  # upper bound safety

    count = load_state().get("count", 0)

    if count >= target:
        print("Reached today's limit")
        return

    # probability per hour (~spread commits across day)
    if random.random() < 0.5:
        make_commit()
        save_state(today, count + 1)
        print(f"Committed ({count+1})")
    else:
        print("Skipped this hour")

if __name__ == "__main__":
    main()
