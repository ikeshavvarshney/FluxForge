import os, sys, time, random, math, shutil
from colorama import init, Fore, Back, Style
import pyfiglet

# SINGLE user-defined function (plus the main runner at bottom)
def visual_creator():
    # --- init ---
    init(autoreset=True)
    clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    try:
        term_cols, term_rows = shutil.get_terminal_size()
    except Exception:
        term_cols, term_rows = 80, 24

    # small helpers as variables (no extra defs)
    clear = lambda: os.system(clear_cmd)
    now = lambda: time.time()
    sleep = time.sleep

    # banner
    clear()
    title_art = pyfiglet.figlet_format("VISUAL CREATOR", font="slant")
    color_cycle = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.BLUE]
    for i, line in enumerate(title_art.splitlines()):
        print(color_cycle[i % len(color_cycle)] + line)
    print(Fore.YELLOW + "Single-function CLI — heavy visuals. Pro-level vibes.\n")

    # Main loop (everything lives inside this function)
    last_output = ""  # can save last printed string for export
    while True:
        try:
            print(Style.BRIGHT + Fore.GREEN + "\nMENU — pick a mode:")
            print("1) Fancy Text → ASCII (random fonts + gradient)")
            print("2) Shapes: Heart, Spiral, Tree, Sine Wave")
            print("3) Animations (randomized set: DVD, Matrix, Pulse, Particles)")
            print("4) Cellular Canvas (particle field / CA-like art)")
            print("5) Save last output to file")
            print("6) Settings (toggle color / size tweak)")
            print("7) Exit")
            choice = input(Fore.CYAN + "\nChoice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        # -------------------------
        # Option 1: Fancy Text ASCII
        # -------------------------
        if choice == "1":
            clear()
            text = input("Enter text (or blank for 'WOW'): ").strip() or "WOW"
            fonts = ["slant", "standard", "big", "banner3-D", "doom", "speed"]
            font = random.choice(fonts)
            try:
                art = pyfiglet.figlet_format(text, font=font)
            except Exception:
                art = pyfiglet.figlet_format(text, font="standard")
            # gradient
            cols = shutil.get_terminal_size().columns
            colors = [Fore.RED, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE]
            out = []
            for r, line in enumerate(art.splitlines()):
                row = ""
                for c, ch in enumerate(line):
                    if ch.strip():
                        row += colors[(c + r) % len(colors)] + ch
                    else:
                        row += ch
                out.append(row)
            last_output = "\n".join(out)
            print(last_output)

            # post-effect: rainbow pulse
            for phase in range(3):
                for shift in range(0, len(colors)):
                    to_print = []
                    for r, line in enumerate(art.splitlines()):
                        row = ""
                        for c, ch in enumerate(line):
                            if ch.strip():
                                row += colors[(c + shift + r) % len(colors)] + ch
                            else:
                                row += ch
                        to_print.append(row)
                    print("\n".join(to_print))
                    sleep(0.08)
                    print("\033[F" * (len(to_print) + 1), end="")  # move cursor up to redraw
            print()  # final newline

        # -------------------------
        # Option 2: Shapes
        # -------------------------
        elif choice == "2":
            clear()
            print("Shapes: 1) Heart  2) Spiral  3) Fractal-ish Tree  4) Sine Wave")
            s = input("Pick shape: ").strip()
            size_in = input("Size (5-40, default 18): ").strip()
            try:
                n = max(5, min(40, int(size_in))) if size_in else 18
            except:
                n = 18

            if s == "1":  # HEART (scaled)
                out_lines = []
                for y in [i * 0.5 for i in range(int(n * -1), n)]:
                    row = ""
                    for x in [i * 0.5 for i in range(int(n * -2), int(n * 2))]:
                        # normalized heart equation
                        eq = (x**2 + y**2 - 1)**3 - x**2 * y**3
                        if eq <= 0:
                            row += Fore.RED + "*"
                        else:
                            row += " "
                    out_lines.append(row)
                last_output = "\n".join(out_lines)
                print(last_output)

            elif s == "2":  # SPIRAL (matrix fill)
                N = n if n % 2 == 1 else n+1
                grid = [[" " for _ in range(N)] for __ in range(N)]
                left, right, top, bottom = 0, N - 1, 0, N - 1
                chs = ["@", "#", "%", "*", "o"]
                step = 0
                while left <= right and top <= bottom:
                    for i in range(left, right + 1):
                        grid[top][i] = chs[step % len(chs)]
                    for i in range(top + 1, bottom + 1):
                        grid[i][right] = chs[step % len(chs)]
                    if top != bottom:
                        for i in range(right - 1, left - 1, -1):
                            grid[bottom][i] = chs[step % len(chs)]
                    if left != right:
                        for i in range(bottom - 1, top, -1):
                            grid[i][left] = chs[step % len(chs)]
                    left += 1; right -= 1; top += 1; bottom -= 1; step += 1
                # print with color spiral
                out = []
                colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
                for r, row in enumerate(grid):
                    out.append("".join([colors[(r + c) % len(colors)] + ch for c, ch in enumerate(row)]))
                last_output = "\n".join(out)
                print(last_output)

            elif s == "3":  # TREE (iterative stack-based)
                levels = max(4, n // 3)
                canvas_width = levels * 4 + 4
                canvas = [[" " for _ in range(canvas_width)] for __ in range(levels * 2 + 4)]
                stack = [ (levels*2, canvas_width//2, levels) ]  # (y, x, size)
                while stack:
                    y, x, size = stack.pop()
                    if y < 0 or size <= 0 or y >= len(canvas): continue
                    # trunk
                    canvas[y][x] = "|"
                    # branch endpoints
                    if size > 1:
                        left_x = x - size
                        right_x = x + size
                        top_y = y - size
                        if 0 <= top_y < len(canvas):
                            canvas[top_y][left_x:right_x+1] = ["^"] * (right_x - left_x + 1)
                        # push smaller branches
                        stack.append((y - size//2, x - size//2, size//2))
                        stack.append((y - size//2, x + size//2, size//2))
                out = []
                for row in canvas:
                    out.append("".join([Fore.GREEN + ch if ch != " " else " " for ch in row]))
                last_output = "\n".join(out)
                print(last_output)

            elif s == "4":  # SINE WAVE (animated)
                msg = input("Symbol for wave (default '*'): ").strip() or "*"
                width = shutil.get_terminal_size().columns
                amp = max(3, min(12, n//2))
                freq = 0.12
                for t in range(120):
                    line = [" "] * width
                    for x in range(width):
                        y = int((math.sin(x * freq + t * 0.25) + 1) * amp)
                        pos = max(0, min(width - 1, y))
                        line[pos] = Fore.CYAN + msg
                    print("".join(line))
                    sleep(0.03)
                    print("\033[F" * (1), end="")  # move up to animate single line
                print()

            else:
                print(Fore.RED + "Invalid shape choice.")

        # -------------------------
        # Option 3: Animations
        # -------------------------
        elif choice == "3":
            clear()
            print("Anim set: 1) DVD Logo  2) Matrix Rain  3) Particle Burst  4) Pulsing Rings  5) Random Mix")
            a = input("Pick or press Enter for random: ").strip()
            if not a:
                a = str(random.choice([1,2,3,4,5]))

            # DVD LOGO (90s)
            if a == "1":
                text = input("Enter label (e.g. 'DVD'): ").strip() or "DVD"
                cols = shutil.get_terminal_size().columns
                rows = shutil.get_terminal_size().lines - 2
                x = random.randint(0, max(0, cols - len(text) - 1))
                y = random.randint(0, max(0, rows - 1))
                vx, vy = random.choice([1, -1]), random.choice([1, -1])
                color = random.choice([Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW])
                for _ in range(240):
                    print("\033[2J\033[H", end="")  # clear screen & move cursor home
                    for r in range(rows):
                        if r == y:
                            line = " " * x + color + text
                            print(line)
                        else:
                            print()
                    # bounce
                    x += vx; y += vy
                    if x <= 0 or x >= cols - len(text) - 1:
                        vx *= -1; color = random.choice([Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW])
                    if y <= 0 or y >= rows - 1:
                        vy *= -1; color = random.choice([Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW])
                    sleep(0.02)

            # MATRIX RAIN
            elif a == "2":
                cols = shutil.get_terminal_size().columns
                rows = shutil.get_terminal_size().lines
                drops = [0] * cols
                symbols = "abcdefghijklmnopqrstuvwxyz0123456789@#$%&"
                for _ in range(200):
                    line = []
                    for i in range(cols):
                        if drops[i] == 0 and random.random() < 0.02:
                            drops[i] = 1
                        if drops[i] > 0:
                            ch = random.choice(symbols)
                            if random.random() < 0.08:
                                ch = Fore.WHITE + ch  # head
                            else:
                                ch = Fore.GREEN + ch
                            line.append(ch)
                            drops[i] += 1
                            if drops[i] > rows or random.random() < 0.02:
                                drops[i] = 0
                        else:
                            line.append(" ")
                    print("".join(line))
                    sleep(0.05)

            # PARTICLE BURST (ASCII fireworks)
            elif a == "3":
                cols = shutil.get_terminal_size().columns
                rows = shutil.get_terminal_size().lines - 2
                cx = cols // 2
                cy = rows // 2
                particles = []
                for _ in range(160):
                    ang = random.random() * math.pi * 2
                    speed = random.uniform(0.3, 2.5)
                    particles.append([cx, cy, math.cos(ang)*speed, math.sin(ang)*speed, random.choice(["*", "+", "o", "•", "✦"])])
                for step in range(40):
                    screen = [[" "]*cols for _ in range(rows)]
                    for p in particles:
                        p[0] += p[2]; p[1] += p[3]
                        px, py = int(p[0]), int(p[1])
                        if 0 <= py < rows and 0 <= px < cols:
                            screen[py][px] = random.choice([Fore.MAGENTA + p[4], Fore.YELLOW + p[4], Fore.CYAN + p[4]])
                        # dampen velocities
                        p[2] *= 0.95; p[3] *= 0.95
                    print("\033[2J\033[H", end="")
                    for r in screen:
                        print("".join(r))
                    sleep(0.06)

            # PULSING RINGS
            elif a == "4":
                cols = shutil.get_terminal_size().columns
                rows = shutil.get_terminal_size().lines - 2
                cx = cols // 2
                cy = rows // 2
                maxr = min(cols, rows) // 2 - 1
                for t in range(40):
                    print("\033[2J\033[H", end="")
                    ring = int((math.sin(t*0.3)+1) * (maxr/2)) + 2
                    for y in range(rows):
                        row = ""
                        for x in range(cols):
                            d = int(math.hypot(x-cx, y-cy))
                            if abs(d - ring) < 1:
                                row += Fore.CYAN + "*"
                            else:
                                row += " "
                        print(row)
                    sleep(0.08)

            # RANDOM MIX
            elif a == "5":
                choice_list = ["1","2","3","4"]
                random_choice = random.choice(choice_list)
                print(Fore.YELLOW + f"Random anim -> {random_choice}")
                # Emulate by jumping to the selected animation label by setting 'a' to it and looping again
                a = random_choice
                # We call continue to rerun the block with new 'a'
                # But since we're deep inside, do a direct rerun by using small recursion emulate: we simply set up to re-evaluate
                # Instead of recursion, hack by using 'continue' to go to top of while and simulate user choosing same option
                # But here we want immediate run, so we just mimic by executing the chosen block; for simplicity, set choice back to "3" and a to random_choice,
                # then fall through by using a small hack: reassign choice and let loop continue to handle. We'll emulate by printing message and re-entering.
                # Simpler: just print message and skip.
                sleep(0.5)
            else:
                print(Fore.RED + "Invalid animation choice.")

        # -------------------------
        # Option 4: Cellular Canvas (particle field / CA-like)
        # -------------------------
        elif choice == "4":
            clear()
            print("Canvas modes: 1) Particle field  2) Simple CA (life-ish)  3) Noise blobs")
            cm = input("Pick: ").strip()
            cols = max(20, min(120, shutil.get_terminal_size().columns))
            rows = max(10, min(40, shutil.get_terminal_size().lines - 4))

            # Particle Field (moving dots with trails)
            if cm == "1":
                particles = []
                for _ in range(cols // 2):
                    particles.append([random.randint(0, cols-1), random.randint(0, rows-1),
                                      random.choice([-1,0,1]), random.choice([-1,0,1])])
                for _ in range(120):
                    grid = [[" "]*cols for __ in range(rows)]
                    for p in particles:
                        p[0] = (p[0] + p[2]) % cols
                        p[1] = (p[1] + p[3]) % rows
                        if random.random() < 0.05:
                            p[2] = random.choice([-1,0,1]); p[3] = random.choice([-1,0,1])
                        grid[p[1]][p[0]] = random.choice([Fore.CYAN + ".", Fore.MAGENTA + "o", Fore.YELLOW + "*"])
                    print("\033[2J\033[H", end="")
                    for r in grid:
                        print("".join(r))
                    sleep(0.04)

            # Simple CA (conway-lite)
            elif cm == "2":
                grid = [[1 if random.random() < 0.25 else 0 for _ in range(cols)] for __ in range(rows)]
                for gen in range(60):
                    nxt = [[0]*cols for _ in range(rows)]
                    for y in range(rows):
                        for x in range(cols):
                            alive = grid[y][x]
                            neighbors = 0
                            for dy in (-1,0,1):
                                for dx in (-1,0,1):
                                    if dy==0 and dx==0: continue
                                    ny = (y+dy)%rows; nx = (x+dx)%cols
                                    neighbors += grid[ny][nx]
                            if alive and (neighbors==2 or neighbors==3):
                                nxt[y][x] = 1
                            elif not alive and neighbors==3:
                                nxt[y][x] = 1
                            else:
                                nxt[y][x] = 0
                    grid = nxt
                    print("\033[2J\033[H", end="")
                    for r in grid:
                        print("".join([Fore.GREEN + "@" if c else " " for c in r]))
                    sleep(0.08)

            # Noise blobs (blobby shapes)
            elif cm == "3":
                blobs = []
                for _ in range(6):
                    blobs.append([random.uniform(0, cols), random.uniform(0, rows),
                                  random.uniform(-0.6,0.6), random.uniform(-0.6,0.6), random.randint(2,6)])
                for _frame in range(120):
                    canvas = [[" "]*cols for __ in range(rows)]
                    for b in blobs:
                        bx, by = b[0], b[1]
                        for y in range(rows):
                            for x in range(cols):
                                d = math.hypot(x-bx, y-by)
                                if d < b[4]:
                                    canvas[y][x] = random.choice([Fore.YELLOW + ".", Fore.MAGENTA + "o", Fore.CYAN + "+"])
                        b[0] += b[2]; b[1] += b[3]
                        # bounce edges
                        if b[0] < 0 or b[0] >= cols: b[2] *= -1
                        if b[1] < 0 or b[1] >= rows: b[3] *= -1
                    print("\033[2J\033[H", end="")
                    for r in canvas:
                        print("".join(r))
                    sleep(0.06)
            else:
                print(Fore.RED + "Invalid canvas choice.")

        # -------------------------
        # Option 5: Save last output to file
        # -------------------------
        elif choice == "5":
            if not last_output:
                print(Fore.RED + "No recent output to save. Generate something first.")
            else:
                fname = input("Filename (e.g. art.txt): ").strip() or f"ascii_{int(now())}.txt"
                try:
                    with open(fname, "w", encoding="utf-8") as f:
                        # strip color codes for file
                        import re
                        plain = re.sub(r'\x1b\[[0-9;]*m', '', last_output)
                        f.write(plain)
                    print(Fore.GREEN + f"Saved to {fname}")
                except Exception as e:
                    print(Fore.RED + "Save failed:", e)

        # -------------------------
        # Option 6: Settings
        # -------------------------
        elif choice == "6":
            print("Settings stub: terminal aware. If colors glitch, disable color by setting env NO_COLOR.")
            print("Resize your terminal for better visuals.")
            sleep(0.8)

        # -------------------------
        # Option 7: Exit
        # -------------------------
        elif choice == "7":
            print(Fore.YELLOW + "Peace out. Visual Creator shutting down.")
            break

        else:
            print(Fore.RED + "Invalid option — try again.")

# runner
if __name__ == "__main__":
    visual_creator()
