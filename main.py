import splash
from wizard import Wizard
import my_connector
import display
def main():
    connector=my_connector
    disp=display
    continu=splash.splashscreen()
    if continu==True:
      wizard = Wizard(connector,disp)
      wizard.start_wizard()

if __name__ == "__main__":
    main()


