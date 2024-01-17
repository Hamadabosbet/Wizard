from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from colorama import Fore
from colorama import Style
def splashscreen():
    md1 = f"""


 
                {Fore.GREEN}          Welcome To Wizard Registration                    
                                                                                                      
                                                                                                                 
                                                                                                                     
                                                                                                                     
                                                                                                                     
                                                                                                                     
                                                                                                                                 {Style.RESET_ALL}

                                 """
    console = Console(record=True)
    panel_1 = Panel(Markdown(md1), width=80,height=5)
    panel_2=Panel(panel_1)




    # Change the color of panel_2
    panel_2 = Panel(panel_1, style="on green")
    # Change "on green" to your desired color combination

    # Display the columns with panel_2
    console.print(Columns([panel_2]))
    print(Style.RESET_ALL)
    while True:
        m = input("if you want to start type start:")
        if m == "start":
           return True

