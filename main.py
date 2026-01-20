import subprocess
import random
import time
import os


def flower(x, y, commits, canvas):
    for i, commit in enumerate(commits,):
    # grow upward one cell per commit
        if y <= 0:
            break

        canvas[y][x] = "|"
        canvas[y][x+1] = "|"
        y -= 1

        if i % 4 == 0:
            x += random.randint(-1,1)

        if i % random.randint(5, 8):
            canvas[y-3][x+1] = "/"
        elif i % random.randint(3, 6):
            canvas[y-1][x-1] = "\\"

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

WIDTH = 60
HEIGHT = 25

def clear():
    os.system("cls" if os.name == "nt" else "clear")

canvas = [[" "] * WIDTH for _ in range(HEIGHT)]

x = WIDTH // 2
y = HEIGHT - 1

# 1 = seed

# 2-3 = stem

# 4-7 = flower
flower(x, y, commits, canvas)

# 8 or more = tree
