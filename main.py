import subprocess
import random
import os
import math
import msvcrt

node_positions = {} 
selected_node = 0 

# colors
SEED_BROWNS = [
    "\033[38;5;94m",  # Original Brown
    "\033[38;5;52m",  # Dark Chocolate / Deep Brown
    "\033[38;5;131m", # Muted Red-Brown
    "\033[38;5;178m", # Ochre / Dark Gold
    "\033[38;5;101m", # Olive-Brown / Khaki
]

BROWN = "\033[38;5;94m"

GREEN = "\033[32m"

PINK = "\033[38;5;211m"

YELLOW = "\033[38;5;184m"

RESET = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_commit_info(commit):
    clear()
    print("Commit:", commit["hash"])
    print("Author:", commit["author"])
    print("Date:  ", commit["date"])
    print()
    print(commit["subject"])
    if commit["body"].strip():
        print("\n" + commit["body"])
    input("\nPress Enter to return")
    msvcrt.getch

def get_git_commits():
    try:
        result = subprocess.run(
            [
                "git", "log",
                "--all",
                "--date=iso",
                "--pretty=format:%H%x1f%an%x1f%ad%x1f%s%x1f%b%x1e"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for record in result.stdout.strip("\n\x1e").split("\x1e"):
            fields = record.split("\x1f")
            commits.append({
                "hash": fields[0],
                "author": fields[1],
                "date": fields[2],
                "subject": fields[3],
                "body": fields[4],
            })
        return commits

    except Exception:
        return [{
            "hash": "dummy",
            "author": "you",
            "date": "",
            "subject": "initial commit",
            "body": ""
        }]

def seed_interaction(x, y, commits, canvas):
    while True:
        key = msvcrt.getch()

        if key == b'\x03':
            raise KeyboardInterrupt
        
        elif key == b'\r':  
            show_commit_info(commits[0])
            seed(x, y, commits, canvas)
            break

        elif key in (b'q', b'Q'):
            break

def seed(x, y, commits, canvas):
    brown = random.choice(SEED_BROWNS)

    sprout_x = x + 19
    sprout_y = y - 2

    canvas[sprout_y][sprout_x] = f"{GREEN}\\|{RESET}"
    canvas[y-1][x+17] = f"{brown}_-~A~-_{RESET}"
    
    soil_text = "~~-^-~---~-^---~/       \\-~-^-~---~--~^-~"

    node_positions[(sprout_x, sprout_y)] = 0
    
    soil_cells = []
    for char in soil_text:
        if char == " ":
            soil_cells.append(" ")
        else:
            soil_cells.append(f"{random.choice(SEED_BROWNS)}{char}{RESET}")

    
    for i, cell in enumerate(soil_cells):
        if x + i < WIDTH:
            canvas[y][x + i] = cell


    
    view_start = max(0, y - 10)
    view_end = min(HEIGHT, y + 30)
    for row in canvas[view_start:view_end]: 
        print("".join(row))
    
    seed_interaction(x, y, commits, canvas)

def sprout(x, y, commits, canvas):
    total_commits = len(commits)

    for i in range(total_commits):

        if i != 0 and i != (total_commits-1) and random.random() > .65:
            side = random.choice(["left", "right"])

            if side == "left":
                canvas[y][x-3] = f"{GREEN}<%\\{BROWN}|"
            elif side == "right":
                canvas[y][x] = f"{BROWN}|{GREEN}/%>"
            else:
                canvas[y][x] = "\033[38;5;94m|"
        elif i == total_commits-1:
            canvas[y][x-2] = f"{GREEN}@\\|%>"
            canvas[y+1][x-3] = f"{GREEN}@"
        else:
            canvas[y][x] = f"{BROWN}|"

        
        y -= 1
        clear()

        view_start = max(0, y - 10)
        view_end = min(HEIGHT, y + 30)
        for row in canvas[view_start:view_end]: 
            print("".join(row))


def flower(x, y, commits, canvas):
    total_commits = len(commits)
    branch_interval = max(1, total_commits // 4)
    leaf_interval = max(1, total_commits // 4)
    thickness = max(2, total_commits // 8)

    for i, commit in enumerate(commits):
        if y <= 15:
            break

        ran = 0
        if i % branch_interval == 0 and i != 0 and total_commits >= 10:
            ran = random.randint(-1, 1)

        char = f"{GREEN}|"
        if ran == -1: char = f"{GREEN}\\"
        elif ran == 1: char = f"{GREEN}/"

        if total_commits > 10:
            for t in range(thickness):
                if 0 <= x + t < WIDTH:
                    canvas[y][x + t] = char

            if i % leaf_interval == 0 and i != 0:
                side = random.choice([-1, thickness])
                if 0 <= x + side < WIDTH: 
                    canvas[y][x + side] = "\033[38;5;22m%"
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
                        canvas[draw_y][draw_x] = f"{PINK}#" 
                    else:
                        canvas[draw_y][draw_x] = f"{YELLOW}+"

    clear()
    first_row = 0
    for idx, row in enumerate(canvas):
        if "".join(row).strip():
            first_row = idx
            break
            
    for row in canvas[first_row:]:
        print("".join(row))


if __name__ == "__main__":

    WIDTH = 100
    HEIGHT = 100
    canvas = [[" "] * WIDTH for _ in range(HEIGHT)]
    commits = get_git_commits()
    commits.reverse()

    try:
        # seed - 1
        # seed(WIDTH // 2, HEIGHT - 1, commits, canvas,)

        # sprout - 2-10
        # sprout(WIDTH // 2, HEIGHT - 1, commits, canvas)

        # flower - 11-20
        flower(WIDTH // 2, HEIGHT - 1, commits, canvas)

        # tree - >21
    except KeyboardInterrupt:
        pass
    finally:
        # reset
        print(RESET)

# C:\Users\Ezra\Downloads\Lingual-Project
# C:\Users\Ezra\Downloads\Games\GitTree\GitTree