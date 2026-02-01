import subprocess
import random
import os
import math
import msvcrt

node_positions = {} 
selected_node = 0 

nodes = list(node_positions.items())
nodes.sort(key=lambda n: n[1]) 



# colors
SEED_BROWNS = [
    "\033[38;5;94m",  # Original Brown
    "\033[38;5;52m",  # Deep Brown
    "\033[38;5;131m", # Muted Red-Brown
    "\033[38;5;178m", # Ochre 
    "\033[38;5;101m", # Khaki
]

TREE_GREENS = [
    "\033[38;5;22m", # Dark Green
    "\033[38;5;28m", # Normal
    "\033[38;5;58m", # Olive Green
    "\033[38;5;29m", # Teal Green
    "\033[38;5;64m", # Mossy Green
    "\033[38;5;22m", #Lighter 
]

BROWN = "\033[38;5;94m"

GREEN = "\033[32m"

PINK = "\033[38;5;211m"

PURPLE = "\033[1;35m"

YELLOW = "\033[38;5;184m"

RED = "\033[38;5;196m"

ORANGE = "\033[38;5;208m"

RESET = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def count():
    try:
        result = subprocess.run(
            ["git", "rev-list", "--all", "--count"],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
    except Exception:
        return 0

def navigate(commits, canvas):
    global selected_node
    nodes = list(node_positions.items())
    nodes.sort(key=lambda n: n[0][1], reverse=True) 

    if not nodes:
        return

    while True:
        clear()
        print("\033[H", end="")
        (x, y), idx = nodes[selected_node]

        window_height = 30 
        view_start = max(0, y - (window_height // 2))
        view_end = min(HEIGHT, view_start + window_height)

        for row_idx in range(view_start, view_end):
            if row_idx == y:
                formatted_line = ""
                for col_idx, char in enumerate(canvas[row_idx]):
                    if col_idx == x:
                        formatted_line += f"{RESET}◉{RESET}"
                    else:
                        formatted_line += char
                print(formatted_line)
            else:
                print("".join(canvas[row_idx]))

        print(f"\n{YELLOW}Node: {selected_node + 1}/{len(nodes)} | "
              f"Commit: {commits[idx]['hash'][:7]} | {commits[idx]['subject']}{RESET}")
        print("(W/S or Arrows to move, Enter for info, Q to quit)")

        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()
            if key == b'H': selected_node = min(len(nodes) - 1, selected_node + 1) # up
            elif key == b'P': selected_node = max(0, selected_node - 1) # down
        elif key == b'w': selected_node = min(len(nodes) - 1, selected_node + 1)
        elif key == b's': selected_node = max(0, selected_node - 1)
        elif key == b'\r': show_commit_info(commits[idx])
        elif key in (b'q', b'Q'): break


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
    msvcrt.getch()

def get_git_commits(limit=None):
    cmd = [
        "git", "log",
        "--all",
        "--date=iso",
        "--pretty=format:%H%x1f%an%x1f%ad%x1f%s%x1f%b%x1f%P%x1e"
    ]

    if limit:
        cmd.insert(2, f"-{limit}")

    result = subprocess.run(
        cmd,
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

    brown = random.choice(SEED_BROWNS)

    sprout_x = x + 19
    sprout_y = y - 2

    canvas[y-1][x+5] = f"{brown}__A__{RESET}"
    anthill_text = "---~/``@``\\-~^-"

    node_positions[(sprout_x, sprout_y)] = 0
    
    soil_cells = []
    for char in anthill_text:
        if char == " ":
            soil_cells.append(" ")
        else:
            soil_cells.append(f"{random.choice(SEED_BROWNS)}{char}{RESET}")

    
    for i, cell in enumerate(soil_cells):
        if x + i < WIDTH:
            canvas[y][x + i] = cell


    total_commits = len(commits)

    for i in range(total_commits):
        node_positions[(x, y)] = i

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
            node_positions[(x, y)] = i

        
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


    brown = random.choice(SEED_BROWNS)

    sprout_x = x + 19
    sprout_y = y - 2

    canvas[y-1][x+thickness+5] = f"{brown}__A__{RESET}"
    anthill_text = "---~/``@``\\-~^-"

    node_positions[(sprout_x, sprout_y)] = 0
    
    soil_cells = []
    for char in anthill_text:
        if char == " ":
            soil_cells.append(" ")
        else:
            soil_cells.append(f"{random.choice(SEED_BROWNS)}{char}{RESET}")

    
    for i, cell in enumerate(soil_cells):
        if x + i < WIDTH:
            canvas[y][x + i+thickness] = cell

    for i, commit in enumerate(commits):
        if y <= 15:
            break

        node_positions[(x, y)] = i

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
            node_positions[(x, y)] = i
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
                draw_y = y + i - 3
                draw_x = center_x + j
                if 0 <= draw_y < HEIGHT and 0 <= draw_x < WIDTH:
                    if (j / (radius * 2))**2 + (i / radius)**2 > 0.8:
                        canvas[draw_y][draw_x] = f"{PINK}#" 
                    else:
                        canvas[draw_y][draw_x] = f"{YELLOW}+"


def tree(x, y, commits, canvas):
    total_commits = len(commits)
    thickness = max(2, total_commits // 4)

    brown = random.choice(SEED_BROWNS)

    sprout_x = x + 19
    sprout_y = y - 2

    canvas[y-1][x+thickness+4] = f"{brown}__A__{RESET}"
    anthill_text = "---~/``@``\\-~^-"

    node_positions[(sprout_x, sprout_y)] = 0
    
    soil_cells = []
    for char in anthill_text:
        if char == " ":
            soil_cells.append(" ")
        else:
            soil_cells.append(f"{random.choice(SEED_BROWNS)}{char}{RESET}")

    
    for i, cell in enumerate(soil_cells):
        if x + i < WIDTH:
            canvas[y][x + i+thickness] = cell


    for i, commit in enumerate(commits):
        if i == 0:
            canvas[y][x-1] = f"{BROWN}/"
            canvas[y][x + thickness + 1] = f"{BROWN}\\"
        else:
            num = random.random()
            if num < .3:
                canvas[y][x] = f"{BROWN}|"
                canvas[y][x + thickness] = f"{BROWN}|"
            elif num > .3 and num < .6:
                canvas[y][x] = f"{BROWN}|"
                canvas[y][x + thickness] = f"{BROWN}|/"
            else:
                canvas[y][x-1] = f"{BROWN}\\|"
                canvas[y][x + thickness - 1] = f"{BROWN}|"
                canvas[y][x + thickness - random.randint(1,thickness)] = f"{random.choice([PURPLE, PINK, RED])}*"

            
            center_x = x + (thickness // 2)
            node_positions[(center_x, y)] = i 

        y -= 1
        
        clear()
        view_start = max(0, y - 10)
        view_end = min(HEIGHT, y + 30)
        for row in canvas[view_start:view_end]: 
            print("".join(row))

        for idx, row in enumerate(canvas):
            if "".join(row).strip():
                first_row = idx
                break
        
    center_x = x + (thickness // 2)
    radius = max(2, min(total_commits // 4, 8))
    
    first_row = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius * 2, (radius * 2) + 1):
            if (j / (radius * 2))**2 + (i / radius)**2 <= 1.1:
                draw_y = y + i - 6
                draw_x = center_x + j
                if 0 <= draw_y < HEIGHT and 0 <= draw_x < WIDTH:
                    number = random.random()
                    if number < .98:
                        LEAVES = ["@", "#", "&", "%"]
                        canvas[draw_y][draw_x] = f"{random.choice(TREE_GREENS)}{random.choice(LEAVES)}"
                    else:
                        canvas[draw_y][draw_x] = f"{random.choice([RED, ORANGE])}0"

    for row in canvas[view_start:view_end]: 
        print("".join(row))
        

def get_limit(commit_count):
    if commit_count <= 200:
        return None  

    while True:
        clear()
        print(f"{RED}This is a large repo! ({commit_count} commits){RESET}\n")
        print("Rendering all commits may be slow or unreadable.")
        print("Enter how many recent commits to render.")
        print("Press Enter to render ALL commits anyway.\n")

        choice = input("Commit limit: ").strip()

        if choice == "":
            return None 

        try:
            limit = int(choice)
            if limit <= 0:
                raise ValueError
            return limit
        except ValueError:
            print("\nPlease enter a positive number.")
            input("Press Enter to try again...")


if __name__ == "__main__":

    count = count()

    limit = get_limit(count)

    WIDTH = 100
    HEIGHT = 100
    canvas = [[" "] * WIDTH for _ in range(HEIGHT)]
    commits = get_git_commits(limit)
    commits.reverse()
    length = len(commits)

    try:
        # seed - 1
        if length == 1:
            seed(WIDTH // 2, HEIGHT - 1, commits, canvas,)

        # sprout - 2-10
        elif 2 <= length <= 10:
            sprout(WIDTH // 2, HEIGHT - 1, commits, canvas)
            navigate(commits, canvas)

        # flower - 11-20
        elif 11 <= length <= 20:
            flower(WIDTH // 2, HEIGHT - 1, commits, canvas)
            navigate(commits, canvas)

        # tree - >21
        else:
            tree(WIDTH // 2, HEIGHT - 1, commits, canvas)
            navigate(commits, canvas)

    except KeyboardInterrupt:
        pass
    finally:
        print(RESET) # reset
