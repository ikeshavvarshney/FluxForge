import os, random, time
from colorama import Fore, Style, init
import pyfiglet

def ascii_visual_creator():
    init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + pyfiglet.figlet_format("ASCII Visual Creator", font="slant"))
    print(Fore.YELLOW + "Welcome to the Visual Creation Terminal!\n")

    while True:
        print(Fore.GREEN + "\nChoose an option:")
        print("1. Text to ASCII Art")
        print("2. Draw Shapes")
        print("3. Generate Random Pattern")
        print("4. Create ASCII Bar Chart")
        print("5. Animation Effect")
        print("6. Clear Screen")
        print("7. Exit")

        choice = input(Fore.CYAN + "\nEnter choice: ")

        # ---------- TEXT TO ASCII ----------
        if choice == '1':
            text = input(Fore.YELLOW + "Enter text: ")
            font = random.choice(['slant', 'standard', 'digital', 'banner3-D'])
            result = pyfiglet.figlet_format(text, font=font)
            print(Fore.MAGENTA + result)

        # ---------- SHAPE GENERATOR ----------
        elif choice == '2':
            print(Fore.CYAN + "\nShapes: 1. Triangle  2. Diamond  3. Spiral")
            shape = input(Fore.YELLOW + "Choose shape: ")
            size = int(input("Enter size (3-20): "))

            if shape == '1':
                for i in range(1, size+1):
                    print(Fore.BLUE + " " * (size-i) + "*" * (2*i-1))
            elif shape == '2':
                for i in range(1, size+1):
                    print(Fore.RED + " " * (size-i) + "*" * (2*i-1))
                for i in range(size-1, 0, -1):
                    print(Fore.RED + " " * (size-i) + "*" * (2*i-1))
            elif shape == '3':
                for i in range(size):
                    print(Fore.GREEN + "*" * ((i % 4) + 1) + " " * (size - i) + "*" * ((i % 3) + 1))
            else:
                print(Fore.RED + "Invalid shape!")

        # ---------- RANDOM PATTERN ----------
        elif choice == '3':
            chars = ['#', '*', '+', '@', '%', '&']
            rows = int(input("Rows: "))
            cols = int(input("Cols: "))
            print(Fore.CYAN + "\nRandom Pattern:\n")
            for i in range(rows):
                line = ''.join(random.choice(chars) for _ in range(cols))
                print(Fore.MAGENTA + line)

        # ---------- BAR CHART ----------
        elif choice == '4':
            n = int(input(Fore.YELLOW + "How many bars? "))
            data = []
            for i in range(n):
                val = int(input(f"Enter value {i+1}: "))
                data.append(val)

            print(Fore.GREEN + "\nASCII Bar Chart:\n")
            max_val = max(data)
            for i, val in enumerate(data):
                bar = "#" * (val * 40 // max_val)
                print(Fore.CYAN + f"Bar {i+1}: " + Fore.YELLOW + bar + f" ({val})")

        # ---------- ANIMATION ----------
        elif choice == '5':
            text = input(Fore.YELLOW + "Enter animation text: ")
            print(Fore.CYAN + "Animating...")
            for i in range(3):
                for frame in ['|', '/', '-', '\\']:
                    print(Fore.GREEN + f"\r{frame} {text} {frame}", end="")
                    time.sleep(0.1)
            print(Fore.MAGENTA + "\nDone!")

        # ---------- CLEAR ----------
        elif choice == '6':
            os.system('cls' if os.name == 'nt' else 'clear')

        # ---------- EXIT ----------
        elif choice == '7':
            print(Fore.YELLOW + "\nThanks for using ASCII Visual Creator!")
            break

        else:
            print(Fore.RED + "Invalid choice! Try again.")

# Run the single function
ascii_visual_creator()
