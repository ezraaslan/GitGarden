WIDTH = 40
HEIGHT = 20

canvas = [[" "]*WIDTH for _ in range(HEIGHT)]

for y in range(5, 15):
    canvas[y][20] = "|"

for row in canvas:
    print("".join(row))
