from colorama import Fore, Style
from tabulate import tabulate

rest=False

def display_summary(details):
    global rest
    show_phase(1, details)
    show_phase(2, details)
    show_phase(3, details)
    show_phase(4, details)

    rest_button=input(f"{Fore.YELLOW} \nenter 1 if you want to rest   or enter to back to Menu ")
    if rest_button=="1":
        rest=True
    elif rest_button == 2:
        pass


def show_phase(num_phase,details):
    phase_functions = {
        1: lambda: print_items(1,details, 0, 3),
        2: lambda: print_items(2,details, 3, 6),
        3: lambda: print_items(3,details, 6, 8),
        4: lambda: print_items(4,details, 8, 11)
    }
    phase_functions.get(num_phase, lambda: print("Invalid phase number"))()


def print_items(num_phase,details, start, end):
    table_data = []
    for key, value in list(details.items())[start:end]:
        table_data.append([f'{Fore.BLUE}{key}:{Fore.LIGHTRED_EX}', value])

    table = tabulate(table_data, headers=["Item", "Value"], tablefmt="grid", colalign=("left", "right"))
    print(f'{Fore.GREEN}Phase {num_phase} items:\n')
    print(table)
    print(Style.RESET_ALL)

def get_rest():

    return rest
