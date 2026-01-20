import subprocess
import random
import time
import os


def flower(x, y, commits, canvas):
    branch_interval = max(1, len(commits) // 5)
    for i, commit in enumerate(commits):
        if y <= 0:
            break

        if i % branch_interval == 0 and i != 0:
            ran = random.randint(-1,1)
            if ran == -1:
                canvas[y][x] = "\\"
                if x+1 < len(canvas[0]):
                    canvas[y][x+1] = "\\"
            elif ran == 1:
                canvas[y][x] = "/"
                if x+1 < len(canvas[0]):
                    canvas[y][x+1] = "/"
            else:
                canvas[y][x] = "|"
                if x+1 < len(canvas[0]):
                    canvas[y][x+1] = "|"
            x += ran
        else:
            canvas[y][x] = "|"
            if x+1 < len(canvas[0]):
                canvas[y][x+1] = "|"
        y -= 1

        clear()
        for row in canvas:
            print("".join(row))
        time.sleep(0.05)


def get_git_commits():
    result = subprocess.run(
        ["git", "log", "--all", "--pretty=format:%H\t%P\t%D"],
        capture_output=True,
        text=True
    )
    commits = []
    for line in result.stdout.splitlines():
        commit, parents, refs = line.split("\t")
        commits.append({
            "id": commit,
            "parents": parents.split() if parents else [],
            "refs": refs
        })
    return commits

commits = get_git_commits()
commits.reverse()

WIDTH = 100
HEIGHT = 100

def clear():
    os.system("cls" if os.name == "nt" else "clear")

canvas = [[" "] * WIDTH for _ in range(HEIGHT)]

x = WIDTH // 2
y = HEIGHT - 1

# 1 = seed

# 2-10 = stem

# 11-20 = flower
flower(x, y, commits, canvas)

# 21 or more = tree
