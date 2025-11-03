import os, time, math, random
from colorama import Fore, Style, init
import pyfiglet

def visual_creator():
    init(autoreset=True)
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

    def gradient_text(text, colors):
        out = ""
        for i, ch in enumerate(text):
            out += colors[i % len(colors)] + ch
        return out + Style.RESET_ALL

    def show_banner(txt):
        fonts = ["slant", "banner3-D", "digital", "doom", "starwars", "speed", "standard"]
        f = random.choice(fonts)
        ascii_art = pyfiglet.figlet_format(txt, font=f)
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
        lines = ascii_art.splitlines()
        for line in lines:
            print(gradient_text(line, colors))
            time.sleep(0.03)

    def fancy_animation(msg, cycles=3):
        width = os.get_terminal_size().columns
        colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.BLUE]
        wave = [math.sin(i/3) for i in range(100)]
        for c in range(cycles):
            for i in range(width - len(msg)):
                offset = int((math.sin(i/5 + c) + 1) * 5)
                color = colors[i % len(colors)]
                print(color + " " * i + msg + " " * offset, end="\r")
                time.sleep(0.01)
            for i in range(width - len(msg), 0, -1):
                offset = int((math.sin(i/5 + c) + 1) * 5)
                color = colors[i % len(colors)]
                print(color + " " * i + msg + " " * offset, end="\r")
                time.sleep(0.01)
        print()

    def ascii_fireworks():
        clear()
        width = os.get_terminal_size().columns
        height = 20
        symbols = ["*", "+", ".", "o", "•", "✦", "✸"]
        colors = [Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.GREEN]
        for _ in range(30):
            clear()
            for y in range(height):
                line = ""
                for x in range(width // 2):
                    if random.random() < 0.02:
                        line += random.choice(colors) + random.choice(symbols)
                    else:
                        line += " "
                print(line)
            time.sleep(0.1)

    def fractal_tree(level, max_level, branch="|"):
        if level > max_level: return
        print(" " * (max_level - level) + Fore.GREEN + branch)
        fractal_tree(level+1, max_level, "/" + "\\"*(level%2))

    print(Fore.CYAN + Style.BRIGHT + pyfiglet.figlet_format("VISUAL CREATOR", font="slant"))
    print(Fore.YELLOW + "Make ASCII come alive\n")

    while True:
        print(Fore.GREEN + "\nMenu:")
        print("1. Text → Fancy ASCII")
        print("2. Cool Shapes (Heart / Spiral / Wave / Fireworks / Tree)")
        print("3. Random Pattern Grid")
        print("4. Animated Text Wave")
        print("5. Exit")

        choice = input(Fore.CYAN + "\nEnter choice: ")

        if choice == "1":
            txt = input("Enter your text: ")
            show_banner(txt)
            fancy_animation(txt)

        elif choice == "2":
            print(Fore.YELLOW + "\nShapes:\n1. Heart  2. Spiral  3. Wave  4. Fireworks  5. Tree")
            s = input("Pick: ")
            n = int(input("Size (5–20): "))

            if s == "1":
                for y in range(int(-n/2), n//2):
                    row = ""
                    for x in range(-n, n+1):
                        eq = (x**2 + y**2 - 1)**3 - x**2 * y**3
                        row += random.choice([Fore.RED, Fore.MAGENTA]) + "*" if eq <= 0 else " "
                    print(row)
            elif s == "2":
                grid = [[" "]*n for _ in range(n)]
                left, right, top, bottom = 0, n-1, 0, n-1
                while left <= right and top <= bottom:
                    for i in range(left, right+1): grid[top][i] = "#"
                    for i in range(top+1, bottom+1): grid[i][right] = "#"
                    for i in range(right-1, left-1, -1): grid[bottom][i] = "#"
                    for i in range(bottom-1, top, -1): grid[i][left] = "#"
                    left+=1; right-=1; top+=1; bottom-=1
                for r in grid: print(Fore.CYAN + "".join(r))
            elif s == "3":
                for x in range(60):
                    y = int((math.sin(x/3.0)+1)*n/2)
                    print(" "*y + random.choice([Fore.CYAN, Fore.YELLOW, Fore.MAGENTA]) + "*")
                    time.sleep(0.03)
            elif s == "4":
                ascii_fireworks()
            elif s == "5":
                fractal_tree(0, n//3)
            else:
                print("Invalid shape!")

        elif choice == "3":
            rows = int(input("Rows: ")); cols = int(input("Cols: "))
            symbols = ['#','@','*','+','%','&']
            for _ in range(rows):
                line = "".join(random.choice(symbols) for _ in range(cols))
                print(random.choice([Fore.CYAN, Fore.YELLOW, Fore.MAGENTA]) + line)
                time.sleep(0.02)

        elif choice == "4":
            msg = input("Enter animation text: ")
            fancy_animation(msg, 5)

        elif choice == "5":
            print(Fore.YELLOW + "\nSee ya!")
            break
        else:
            print(Fore.RED + "Invalid input.")

if __name__ == "__main__":
    visual_creator()
