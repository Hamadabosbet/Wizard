from phase import Phase
from typing import List, Dict, Union, Any


class Wizard:
    def __init__(self,connector,display) -> None:
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
        self.connector = connector
        self.display = display
        self.phases: List[Phase] = []
        self.wizards: List[Dict[str, Union[str, None]]] = []

    def check_if_update(self, phase: Phase) -> None:
        if_update = input("Do you want to update something? Type 'Y' for Yes or 'N' for No: ")
        if if_update.upper() == 'Y':
            print("You chose to update something.")
            phase.update(self)
            if isinstance(self.details, list) and len(self.details) > 0:
                self.display.show_phase(phase.num_phase, self.details[0])
            else:
                print("updating successfully")
        elif if_update.upper() == 'N':
            print("You chose not to update anything.")

    def create_phase(self, num_phase: int) -> None:
        print(f"You are in Phase {num_phase}")
        phase = Phase(num_phase)
        phase.run_phase(self)
        if self.details:
            self.display.show_phase(phase.num_phase, self.details)
            self.phases.append(phase)
            self.check_if_update(phase)
        else:
            print("Details not found.")

    def prev_or_next(self, num_phase: int) -> Union[str, None]:
        while True:
            move = input(f"You are in Phase {num_phase}, Type (1) for Next / (2) for Prev / (3) for exit: ")
            if move == "1":
                num_phase = self.handle_next_move(num_phase)
                if num_phase > 3:
                    self.create_phase(num_phase)
                    self.details["is_finished"] = True
                    return 'done'
            elif move == "2":
                num_phase = self.handle_prev_move(num_phase)
            elif move == "3":
                self.details["is_finished"] = False
                return "done"
            else:
                print("Invalid choice. Please enter '1' to continue Next, '2' to Prev, or '3' to exit.")

    def handle_next_move(self, num_phase: int) -> int:
        num_phase += 1
        self.create_phase(num_phase)
        return num_phase

    def handle_prev_move(self, num_phase: int) -> int:
        if num_phase == 1:
            print('You are in Phase 1, You cannot go back.')
        else:
            num_phase -= 1
            self.display.show_phase(num_phase, self.details)
            self.check_if_update(self.phases[num_phase - 1])
        return num_phase

    def start_wizard(self) -> None:
        self.connector.connect_to_db()
        print("Welcome to the Wizard!")
        try:
            while True:
                choice = input("Menu: 1) Start New 2) Continue: 3) History 4) Statistics 5) exit")
                if choice == "1":
                    self.start_new_wizard()
                elif choice == "2":
                    self.continue_wizard()
                elif choice == "3":
                    self.connector.show_wizards_history_from_db()
                elif choice == "4":
                    self.connector.show_statistics()
                elif choice == "5":
                    print("you are out")
                    break
                else:
                    print("Invalid choice!")
        finally:
              self.connector.close_db_connection()

    def start_new_wizard(self):
        self.create_phase(1)
        if_done = self.prev_or_next(1)
        if if_done == 'done':
            self.save_wizard_and_display_summary()

    def continue_wizard(self):
        self.connector.show_unfinished_wizards_from_db()
        wizards = self.connector.load_wizards_from_db(is_finished=False)
        if wizards:
            while True:
                chosen_name = input("Enter the name of the wizard you want to continue registration   or 0 to exit: ")
                if chosen_name=="0":
                    break
                chosen_wizard = next((wizard for wizard in wizards if wizard["Name"] == chosen_name), None)
                if chosen_wizard:
                    self.details = chosen_wizard
                    self.process_continue_wizard()
                    break
                else:
                    print(f"No wizard found with the name: {chosen_name}. Try again.")
            else:
                print("No unfinished wizards found.")

    def process_continue_wizard(self):
        phase_number = int(input("Enter phase number: "))
        if phase_number > len(self.phases):
            self.create_phase(phase_number)
            if_done = self.prev_or_next(phase_number)
            if if_done == 'done':
                self.save_wizard_and_display_summary()
        else:
            self.display.show_phase(phase_number, self.details)

    def save_wizard_and_display_summary(self):
        self.connector.save_wizard_to_db(self.details)
        self.display.display_summary(self.details)
        self.phases = []
        self.wizards.append(self.details)
        self.details = {}









