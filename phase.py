import re
from typing import Callable

class Phase:
    def __init__(self, number: int) -> None:
        self.num_phase: int = number

        self.validation_functions: dict[str, Callable[[str], bool]] = {
            "Name": lambda x: len(x.split()) == 2 and all(len(name) >= 2 for name in x.split()),
            "Email": lambda x: len(x) > 0 and re.match(r"[^@]+@[^@]+\.[^@]+", x),
            "Birth Date": lambda x: len(x) > 0 and len(x.split('/')) == 3,
            "City": lambda x: len(x) > 0,
            "Street": lambda x: len(x) > 0,
            "Number": lambda x: x.isnumeric() and int(x) != 0 and int(x) > 0,
            "Social Media": lambda x: bool(re.compile(r'^(https?://)?(www\.)?(facebook|twitter|instagram|linkedin)\.com/.*$').match(x)),
            "Hobbies": lambda x: True,
            "Happy": lambda x: x == 'Yes' or x == 'No',
            "Skydiving": lambda x: x == 'Yes' or x == 'Maybe' or x == 'No',
            "One Dollar": lambda x: x == 'Yes' or x == 'No'
        }

    def input_validation(self, string: str, func: Callable[[str], bool] = None) -> str:
        while True:
            print(string, end='')
            if func:
                user_input = input()
                if func(user_input):
                    return user_input
                else:
                    print("Invalid input. Please enter it again.")
            else:
                user_input = input()
                return user_input

    def run_phase(self, wizard: 'Wizard') -> None:
        if self.num_phase == 1:
            wizard.details["Name"] = self.input_validation('Enter your full name (minimum 2 characters each):\n',
                                                            self.validation_functions["Name"])
            wizard.details["Email"] = self.input_validation('Enter your email address:\n',
                                                             self.validation_functions["Email"])
            wizard.details["Birth Date"] = self.input_validation('Enter your birth date in format (dd/MM/yy):\n',
                                                                  self.validation_functions["Birth Date"])
        elif self.num_phase == 2:
            wizard.details["City"] = self.input_validation('Enter your city\n', self.validation_functions["City"])
            wizard.details["Street"] = self.input_validation('Enter your street\n', self.validation_functions["Street"])
            wizard.details["Number"] = self.input_validation('Enter your number\n', self.validation_functions["Number"])
        elif self.num_phase == 3:
            wizard.details["Social Media"] = self.input_validation(
                'Enter your social media (facebook, twitter, Instagram or linkedin)\n',
                self.validation_functions["Social Media"])
            wizard.details["Hobbies"] = self.input_validation('Enter your hobbies (Chess, Movies, Sport, Cars, Dolls)\n')
        else:
            wizard.details["Happy"] = self.input_validation('Are you a happy person? Yes/No\n',
                                                            self.validation_functions["Happy"])
            wizard.details["Skydiving"] = self.input_validation(' Will you do skydiving? Yes/Maybe/No\n',
                                                                self.validation_functions["Skydiving"])
            wizard.details["One Dollar"] = self.input_validation()

    def update(self, wizard: 'Wizard') -> None:
        choice = input("What field do you want to change?")
        choice = choice.capitalize()

        if self.num_phase == 1:
            self.update_phase_field(wizard, choice, ["Name", "Email", "Birth Date"])
        if self.num_phase == 2:
            self.update_phase_field(wizard, choice, ["City", "Street", "Number"])
        if self.num_phase == 3:
            self.update_phase_field(wizard, choice, ["Social Media", "Hobbies"])
        if self.num_phase == 4:
            self.update_phase_field(wizard, choice, ["Happy", "Skydiving", "One Dollar"])

    def update_phase_field(self, wizard: 'Wizard', choice: str, phase_attributes: list[str]) -> None:
        '''Update a field in the wizard's details if it belongs to the specified phase.

        Args: wizard (Wizard): The wizard instance.
            choice (str): The field the user wants to update.
            phase_attributes (list): List of valid field names for the current phase.

        Returns: None
        '''
        if choice in phase_attributes:
            wizard.details[choice] = self.input_validation(f'Enter your {choice}:\n',
                                                           self.validation_functions[choice])
        else:
            print("Invalid field choice.")