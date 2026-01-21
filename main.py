import subprocess
import random
import os
import math

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def flower(x, y, commits, canvas):
    total_commits = len(commits)
    branch_interval = max(1, total_commits // 5)
    leaf_interval = max(1, total_commits // 10)
    thickness = max(2, total_commits // 8)

    for i, commit in enumerate(commits):
        if y <= 15:
            break

        ran = 0
        if i % branch_interval == 0 and i != 0 and total_commits >= 10:
            ran = random.randint(-1, 1)

        char = "|"
        if ran == -1: char = "\\"
        elif ran == 1: char = "/"

        if total_commits > 10:
            for t in range(thickness):
                if 0 <= x + t < WIDTH:
                    canvas[y][x + t] = char

            if i % leaf_interval == 0 and i != 0:
                if 0 <= x - 1 < WIDTH: canvas[y][x - 1] = "#"
                if 0 <= x + thickness < WIDTH: canvas[y][x + thickness] = "#"
        else:
            canvas[y][x] = char
            canvas[y][x + 1] = char

        x += ran
        y -= 1
        
        clear()
        view_start = max(0, y - 10)
        view_end = min(HEIGHT, y + 30)
        for row in canvas[view_start:view_end]: 
            print("".join(row))

    center_x = x + (thickness // 2)
    radius = max(2, min(total_commits // 8, 8))
    
    for i in range(-radius, radius + 1):
        for j in range(-radius * 2, (radius * 2) + 1):
            if (j / (radius * 2))**2 + (i / radius)**2 <= 1.1:
                draw_y = y + i
                draw_x = center_x + j
                if 0 <= draw_y < HEIGHT and 0 <= draw_x < WIDTH:
                    if (j / (radius * 2))**2 + (i / radius)**2 > 0.8:
                        canvas[draw_y][draw_x] = "#" 
                    else:
                        canvas[draw_y][draw_x] = "+"

    clear()
    first_row = 0
    for idx, row in enumerate(canvas):
        if "".join(row).strip():
            first_row = idx
            break
            
    for row in canvas[first_row:]:
        print("".join(row))



def get_git_commits():
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--pretty=format:%H\t%P\t%D"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.splitlines():
            parts = line.split("\t")
            commits.append({"id": parts[0]})
        return commits
    except Exception:
        return [{"id": i} for i in range(25)]

WIDTH = 100
HEIGHT = 100
canvas = [[" "] * WIDTH for _ in range(HEIGHT)]
commits = get_git_commits()
commits.reverse()

# seed - 1

# stem - 2-10

# flower - 11-20
flower(WIDTH // 2, HEIGHT - 1, commits, canvas)

# tree - >21

# C:\Users\Ezra\Downloads\Lingual-Project
# C:\Users\Ezra\Downloads\Games\GitTree\GitTree