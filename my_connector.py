from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
from typing import List, Dict, Optional, Union

def connect_to_database() -> mysql.connector.MySQLConnection:
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Hamad12345',
        port='3306',
        database='wizard'
    )
    return mydb

def connect_to_db() -> None:
    try:
        mydb = connect_to_database()
        cursor = mydb.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Wizards (
                Name VARCHAR(255) PRIMARY KEY,
                Email VARCHAR(255),
                BirthDate VARCHAR(10),
                City VARCHAR(255),
                Street VARCHAR(255),
                Number VARCHAR(255),
                SocialMedia VARCHAR(255),
                Hobbies ENUM('Chess','Movies','Sport','Cars','Dolls'),
                Happy VARCHAR(5),
                Skydiving VARCHAR(5),
                OneDollar VARCHAR(5),
                isFinished BOOLEAN
            )
        ''')
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        exit()

def close_db_connection() -> None:
    mydb = connect_to_database()
    if mydb.is_connected():
        mydb.cursor().close()
        mydb.close()

def save_wizard_to_db(details: Dict[str, Union[str, bool]]) -> None:
    mydb: Optional[mysql.connector.MySQLConnection] = None
    cursor: Optional[mysql.connector.cursor.MySQLCursor] = None
    try:
        mydb = connect_to_database()
        cursor = mydb.cursor()

        existing_wizards = load_wizards_from_db(is_finished=False)
        existing_wizard = next((wizard for wizard in existing_wizards if wizard["Name"] == details["Name"]), None)

        if existing_wizard:
            cursor.execute('''
                    UPDATE Wizards
                    SET Email=%s, BirthDate=%s, City=%s, Street=%s, Number=%s,
                        SocialMedia=%s, Hobbies=%s, Happy=%s, Skydiving=%s, OneDollar=%s, isFinished=%s
                    WHERE Name=%s
                ''', (
                details["Email"],
                details["Birth Date"],
                details["City"],
                details["Street"],
                details["Number"],
                details["Social Media"],
                details["Hobbies"],
                details["Happy"],
                details["Skydiving"],
                details["One Dollar"],
                bool(details.get("is_finished", False)),
                details["Name"]
            ))
        else:
            cursor.execute('''
                    INSERT INTO Wizards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                details["Name"],
                details["Email"],
                details["Birth Date"],
                details["City"],
                details["Street"],
                details["Number"],
                details["Social Media"],
                details["Hobbies"],
                details["Happy"],
                details["Skydiving"],
                details["One Dollar"],
                bool(details.get("is_finished", False))
            ))

        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

def load_wizards_from_db(is_finished: Optional[bool] = None) -> List[Dict[str, Union[str, bool]]]:
    wizards: List[Dict[str, Union[str, bool]]] = []
    mydb: Optional[mysql.connector.MySQLConnection] = None
    cursor: Optional[mysql.connector.cursor.MySQLCursor] = None
    try:
        mydb = connect_to_database()
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM Wizards WHERE isFinished=%s', (is_finished,))
        rows = cursor.fetchall()
        for row in rows:
            wizard_details = {
                "Name": row[0],
                "Email": row[1],
                "Birth Date": row[2],
                "City": row[3],
                "Street": row[4],
                "Number": row[5],
                "Social Media": row[6],
                "Hobbies": row[7],
                "Happy": row[8],
                "Skydiving": row[9],
                "One Dollar": row[10],
                "is_finished": bool(row[11])
            }
            wizards.append(wizard_details)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

    return wizards

def show_wizards_history_from_db() -> None:
    wizards = load_wizards_from_db(is_finished=True)
    show_wizards(wizards)

def show_unfinished_wizards_from_db() -> None:
    wizards = load_wizards_from_db(is_finished=False)
    show_wizards(wizards)

def show_wizards(wizards: List[Dict[str, Union[str, bool]]]) -> None:
    if not wizards:
        print("No wizards found.")
        return
    headers = list(wizards[0].keys())
    wizards_data = [list(wizard.values()) for wizard in wizards]

    print(tabulate(wizards_data, headers=headers))

def show_statistics() -> None:
    finished_wizards = len(load_wizards_from_db(is_finished=True))
    unfinished_wizards = len(load_wizards_from_db(is_finished=False))
    ages = [calculate_age(wizard["Birth Date"]) for wizard in load_wizards_from_db(is_finished=True)]
    if ages:
        oldest_age = max(ages)
        youngest_age = min(ages)
        average_age = sum(ages) / len(ages)

    hobbies_counts = calculate_hobbies_counts()

    print(f"Finished wizards: {finished_wizards}")
    print(f"Unfinished wizards: {unfinished_wizards}")
    if ages:
        print(f"Oldest age: {oldest_age}")
        print(f"Youngest age: {youngest_age}")
        print(f"Average age: {average_age}")
    print("Hobbies counts:")
    for hobby, count in hobbies_counts.items():
        print(f"{hobby}: {count}")

def calculate_age(birth_date: str) -> int:
    birth_date = datetime.strptime(birth_date, '%d/%m/%y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def calculate_hobbies_counts() -> Dict[str, int]:
    all_wizards = load_wizards_from_db(is_finished=True)
    all_hobbies = [wizard["Hobbies"] for wizard in all_wizards]
    hobbies_counts = {hobby: all_hobbies.count(hobby) for hobby in set(all_hobbies)}
    return hobbies_counts