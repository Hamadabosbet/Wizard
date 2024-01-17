import splash
from wizard import Wizard


def main():
    continu=splash.splashscreen()
    if continu==True:
      wizard = Wizard()
      wizard.start_wizard()

if __name__ == "__main__":
    main()
