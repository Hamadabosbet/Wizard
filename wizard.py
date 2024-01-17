from operator import itemgetter
from tabulate import tabulate
from phase import Phase
import my_connector
import display
from typing import List, Dict, Union, Any


class Wizard:
    def __init__(self) -> None:
        self.details: Dict[str, Any] = {
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
        self.phases: List[Phase] = []
        self.wizards: List[Dict[str, Union[str, None]]] = []

    def check_if_update(self, phase: Phase) -> None:
        if_update = input("Do you want to update something? Type 'Y' for Yes or 'N' for No: ")
        if if_update.upper() == 'Y':
            print("You chose to update something.")
            phase.update(self)
            display.show_phase(phase.num_phase, self.details[0])
        elif if_update.upper() == 'N':
            print("You chose not to update anything.")

    def create_phase(self, num_phase: int) -> None:
        print(f"You in Phase {num_phase}")
        phase = Phase(num_phase)
        phase.run_phase(self)
        display.show_phase(phase.num_phase, self.details)
        self.phases.append(phase)
        self.check_if_update(phase)

    def prev_or_next(self, num_phase: int) -> Union[str, None]:
        while True:
            move = input(f"You in Phase {num_phase} ,Type (1) for Next  / (2) for Prev  /(3) for exit: ")
            if move == "1":
                if num_phase == 1:
                    num_phase += 1
                    self.create_phase(num_phase)
                if num_phase == 2:
                    num_phase += 1
                    self.create_phase(num_phase)

                if num_phase == 3:
                    self.create_phase(num_phase + 1)
                    self.details["is_finished"] = True
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

            elif move == "3":
                self.details["is_finished"] = False
                return "done"
            else:
                print("Invalid choice. Please enter '1' to continue Next or '2' to Prev.")

    def start_wizard(self) -> None:
        my_connector.connect_to_db()
        print("Welcome to the Wizard!")
        while True:
            choice = input("Menu: 1) Start New 2) Continue: 3) History 4) Statistics 5) exit")
            if choice == "1":
                self.create_phase(1)
                if_done = self.prev_or_next(1)
                if if_done == 'done':
                    my_connector.save_wizard_to_db(self.details)
                    display.display_summary(self.details)
                    self.phases = []
                    self.wizards.append(self.details)
                    self.details = {}

            elif choice == "2":
                my_connector.show_unfinished_wizards_from_db()
                wizards = my_connector.load_wizards_from_db(is_finished=False)
                if wizards:
                    while True:
                        chosen_name = input("Enter  the  name of wizard that  you want to continue registration for him: ")
                        if chosen_name:
                            chosen_wizard = next((wizard for wizard in wizards if wizard["Name"] == chosen_name),
                                                 None)
                            if chosen_wizard:
                                self.details = chosen_wizard
                                phase_number = int(input("Enter phase number: "))
                                if phase_number > len(self.phases):
                                    self.create_phase(phase_number)
                                    if_done = self.prev_or_next(phase_number)
                                    if if_done == 'done':
                                        my_connector.save_wizard_to_db(self.details)
                                        display.display_summary(self.details)
                                        self.phases = []
                                        self.wizards.append(self.details)
                                        self.details = {}
                                        break
                                else:
                                    self.show_phase(phase_number, self.details)
                            else:
                                print(f"No wizard found with the name: {chosen_name}. Try again.")
                        else:
                            print("Invalid input. Please enter your full name.")
                else:
                    print("No unfinished wizards found.")
                    return None

            elif choice == "3":
                my_connector.show_wizards_history_from_db()
            elif choice == "4":
                my_connector.show_statistics()
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

        my_connector.close_db_connection()









