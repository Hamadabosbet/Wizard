from operator import itemgetter
from tabulate import tabulate
from phase import Phase
import display

class Wizard:
    def __init__(self):
        self.details = {
            "Name": None,
            "Email": None,
            "Birth Date": None,
            "City": None,
            "Street": None,
            "Number": None,
            "Social Media": None,
            "Hobbies": None,
            "Happy": None,
            "Skydiving": None,
            "One Dollar": None
        }
        self.phases = []
        self.wizards=[]

    def show_wizards_history(self):
        if not self.wizards:
            print("No wizards completed yet.")
            return

        headers = list(self.wizards[0].keys())
        wizards_data = [list(wizard.values()) for wizard in self.wizards]

        print(tabulate(wizards_data, headers=headers))

        while True:
            sort_choice = input("\n\n\nSort by column: (1) Name (2) Email (3) Birth Date (4) City (5) Street "
                                "(6) Number (7) Social Media (8) Hobbies (9) Happy (10) Skydiving (11) One Dollar (0) Cancel: ")
            if sort_choice == "0":
                break
            elif sort_choice.isdigit() and 1 <= int(sort_choice) <= len(headers):
                column_index = int(sort_choice) - 1
                sorted_wizards = sorted(self.wizards, key=itemgetter(headers[column_index]))
                print(tabulate([list(wizard.values()) for wizard in sorted_wizards], headers=headers))
            else:
                print("Invalid choice. Please enter a number between 1 and 11 or '0' to cancel.")




    def check_if_update(self, phase):
        if_update = input("Do you want to update something? Type 'Y' for Yes or 'N' for No: ")
        if if_update.upper() == 'Y':
            print("You chose to update something.")
            phase.update(self)
            display.show_phase(phase.num_phase, self.details[0])
        elif if_update.upper() == 'N':
            print("You chose not to update anything.")

    def create_phase(self, num_phase):
        print(f"You in Phase {num_phase}")
        phase = Phase(num_phase)
        phase.run_phase(self)
        display.show_phase(phase.num_phase, self.details)
        self.phases.append(phase)
        self.check_if_update(phase)

    def prev_or_next(self, num_phase):
        while True:
            move = input(f"You in Phase {num_phase} ,Type (1) for Next  / (2) for Prev : ")
            if move == "1":
                if num_phase == 1:
                    num_phase += 1
                    self.create_phase(num_phase)
                if num_phase == 2:
                    num_phase += 1
                    self.create_phase(num_phase)

                if num_phase == 3:
                    self.create_phase(num_phase + 1)
                    return 'done'
            elif move == "2":
                if num_phase == 1:
                    print('You in Phase 1, You cant prev')
                    display.show_phase(num_phase, self.details)
                    self.check_if_update(self.phases[num_phase - 1])
                elif num_phase == 2:
                    num_phase -= 1
                    print('You in Phase 1')
                    display.show_phase(num_phase, self.details)
                    self.check_if_update(self.phases[num_phase - 1])
                elif num_phase == 3:
                    num_phase -= 1
                    print('You in Phase 2')
                    display.show_phase(num_phase, self.details)
                    self.check_if_update(self.phases[num_phase - 1])
                elif num_phase == 4:
                    print('You in Phase 3')
                    display.show_phase(num_phase - 1, self.details)
                    self.check_if_update(self.phases[num_phase - 2])
            else:
                print("Invalid choice. Please enter '1' to continue Next or '2' to Prev.")

    def start_wizard(self):
        print("Welcome to the Wizard!")
        while True:
            choice = input("Menu: 1) Start New 2) Continue: 3) History ")
            if choice == "1":
                self.create_phase(1)
                if_done = self.prev_or_next(1)
                if if_done == 'done':
                    if display.get_rest()==True:
                        self.details = {}
                    display.display_summary(self.details)
                    self.phases = []
                    self.wizards.append(self.details)
                    self.details={}
            elif choice == "2":
                phase_number = int(input("Enter phase number: "))
                phase_numbers = [phase.num_phase for phase in self.phases]
                if phase_number in phase_numbers:
                    self.show_phase(phase_number, self.details)
                elif phase_number == len(self.phases) + 1:
                    self.create_phase(phase_number)
                else:
                    print("You can't access this phase yet. Please complete previous phases.")
            elif choice == "3":
                self.show_wizards_history()
            else:
                print("Invalid choice!")
