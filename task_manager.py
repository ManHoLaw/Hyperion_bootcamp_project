# =====importing libraries===========
from datetime import datetime
from datetime import date


# ====Login Section====
def login(file):
    """Read the user.txt file and convert it into a dictionary for use

    Args:
        file (txt): File contain the login information

    Returns:
        Dictionary: The dictionary of the user.txt
    """
    usernames = []
    passwords = []
    with open(file, "r") as f:
        for line in f:
            username, password = line.split(", ")
            usernames.append(username)
            passwords.append(password.strip("\n"))
            login_detail = dict(zip(usernames, passwords))
        return login_detail


def check_login(file):
    """Read users input and check if it is in the database

    Args:
        login_detail (dictionary): The database use to check the user input

    Returns:
        Boolean: The check is correct.
    """
    login_detail = login(file)
    while True:
        try:
            username = input("Please enter your username. ")
            password = input("Please enter your password. ")
            if username in login_detail.keys():
                if login_detail[username] == password:
                    print("Login detail correct. Logging in. ")
                    return True, username
                else:
                    print("Login detail incorrect. Please try again. ")

            elif username not in login_detail.keys():
                print("Username not found. Please try again. ")

        except ValueError:
            print("Invalid Input. Please enter you username and password. ")


def register(file):
    """Register user input for a new username and password.

    Args:
        file (.txt): File contain the login information
    """
    username = input("Please enter a new username: ")
    while True:
        password = input("Please enter your password: ")
        password_confirm = input("Please confirm your password: ")
        if password == password_confirm:
            with open(file, "a") as f:
                f.write(f"\n{username}, {password}")
                print(f"\nYou have registered account {username}. ")
                break
        else:
            print("The passwords are different. ")


def new_task(file="tasks.txt"):
    """Take input of user, title, description and date_finish

    Args:
        file (str, optional): File name. Defaults to "tasks.txt".

    Returns:
        Str: Relevant information of the task
    """
    with open(file, "a+") as f:
        user = login("user.txt").keys()
        while True:
            username = input("Please enter your username: ")
            if username in user:
                break
            else:
                print("User do not exist. ")
        title = input("Please enter the title of the task: ")
        description = input("Please enter the description of the task: ")
        input_format = "%d %b %Y"
        date_current = date.today()
        date_current = date_current.strftime(input_format)
        while True:
            try:
                date_finish_input = input(
                    "Please enter the due date of the task. "
                    f"Example: {date_current} ")
                date_finish = datetime.strptime(
                    date_finish_input, input_format).date()
                date_finish = date_finish.strftime(input_format)
                break
            except ValueError:
                print(
                 "Invalid date. Please enter the date in the correct format. ")
        task_status = "No"
        f.write(
            f"\n{username}, {title}, {description}, "
            f"{date_current}, {date_finish}, {task_status}")


def print_task(status, login_username=[], file="tasks.txt"):
    with open(file, "r") as f:
        for line in f:
            username, title, description, \
                    date_current, date_finish, task_status = line.split(", ")
            task = "_" * 100 + \
                f"""\n
                Task:                   {title}
                Assigned to:            {username}
                Date assigned:          {date_current}
                Due date:               {date_finish}
                Task complete?          {task_status}
                Task description:
                {description}\n""" + "_" * 100
            if status == "va":
                print(task)
            elif status == "vm" and username == login_username:
                print(task)


def view_statistics():
    with open("user.txt", "r") as f:
        count_user = sum(1 for line in f)
    with open("tasks.txt", "r") as f:
        count_tasks = sum(1 for line in f)
    print(f"""
          ____________________________________________________

          Number of user registered:         {count_user}
          Number of tasks ongoing:           {count_tasks}
          ____________________________________________________
          """)


file = ("user.txt")
status = False
while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    if status is False:
        status, username = check_login(file)
    elif status is True:
        if username == "admin":
            menu = input('''\nSelect one of the following options:
            r - register a user
            a - add task
            va - view all tasks
            vm - view my tasks
            vs - view all statistic
            e - exit
            : ''').lower()
        else:
            menu = input('''\nSelect one of the following options:
            r - register a user
            a - add task
            va - view all tasks
            vm - view my tasks
            e - exit
            : ''').lower()

        if menu == 'r' and username == "admin":
            print("You have selected to register a new user. ")
            register(file)
            print("")
        elif menu == "r":
            print("Only admin is allow to register a new user. ")

        elif menu == 'a':
            new_task()

        elif menu == 'va':
            print_task("va")

        elif menu == 'vm':
            print_task("vm", username)

        elif menu == "vs" and username == "admin":
            view_statistics()

        elif menu == 'e':
            print('Logging out. Goodbye!!!')
            exit()

        else:
            print("You have entered an invalid input. Please try again")
