import sqlite3
import time


def new_expenses():
    """
    Add new expenses category to the database. Asking the user if
    they would like to would like to add a new category or
    exit back to the main menu. If a user created a new category,
    the user will be prompted to choose whether to add another category.
    """
    cursor_et.execute('SELECT expense_category FROM expense_tracking ')
    expense_category = [row[0] for row in cursor_et.fetchall()]
    while True:
        new_expense = input(
            """Please enter the name of the category you want to add.
* Type exit to go back to the menu.
"""
            ).capitalize()
        if new_expense in expense_category:
            print("Category already in the database. ")
        elif new_expense == 'Exit':
            print("Exiting to main menu. ")
            break
        else:
            cursor_et.execute('''INSERT INTO expense_tracking(
                expense_category, expense)
                    VALUES (?,?)''', (new_expense, 0))
            expense_amount(new_expense)
        exit_status = False
        while True:
            choice = input(
                    "Would you like to add another category? (Y/N) "
                    ).capitalize()
            if choice == "Y":
                break
            elif choice == "N":
                print("Exiting to main menu. ")
                et.commit()
                exit_status = True
                break
            else:
                print("Invalid input.")
        if exit_status:
            break


def expense_amount(category):
    """Take in the category and update the expense with a user input.

    Args:
        category (str): the category currently being viewed.
    """
    while True:
        try:
            expense_amount = int(input("Please enter your expense amount. "))
            cursor_et.execute('''UPDATE expense_tracking SET expense=?
                                WHERE expense_category=?''', (expense_amount,
                                                              category))
            break
        except ValueError:
            print("Invalid input. ")
    et.commit()


def track_spending():
    """Track the total expense for all the category and print the total amount
    and the current category in the database.
    """
    cursor_et.execute('SELECT expense_category FROM expense_tracking ')
    expense_category = [row[0] for row in cursor_et.fetchall()]
    print("Current expense category in the database. ")
    print(expense_category)
    cursor_et.execute('SELECT expense FROM expense_tracking')
    expenses = [int(row[0]) for row in cursor_et.fetchall()]
    total = 0
    for expense in expenses:
        total = total + expense
    print(f"The total spending is {total}.")


def new_income():
    """
    Add new income category to the database. Asking the user if
    they would like to would like to add a new category or
    exit back to the main menu. If a user created a new category,
    the user will be prompted to choose whether to add another category.
    """
    cursor_it.execute('SELECT income_category FROM income_tracking ')
    income_category = [row[0] for row in cursor_it.fetchall()]
    while True:
        new_income = input(
            """Please enter the name of the category you want to add.
* Type exit to go back to the menu.
"""
            ).capitalize()
        if new_income in income_category:
            print("Category already in the database. ")
        elif new_income == 'Exit':
            print("Exiting to main menu. ")
            break
        else:
            cursor_it.execute('''INSERT INTO income_tracking(
                income_category, income)
                    VALUES (?,?)''', (new_income, 0))
            income_amount(new_income)
        exit_status = False
        while True:
            choice = input(
                    "Would you like to add another category? (Y/N) "
                    ).capitalize()
            if choice == "Y":
                break
            elif choice == "N":
                print("Exiting to main menu. ")
                it.commit()
                exit_status = True
                break
            else:
                print("Invalid input.")
        if exit_status:
            break


# update an income amount
def income_amount(category):
    """Take in the category and update the income with a user input.

    Args:
        category (str): the category currently being viewed.
    """
    while True:
        try:
            income_amount = int(input("Please enter your income amount. "))
            cursor_it.execute('''UPDATE income_tracking SET income=?
                                WHERE income_category=?''', (income_amount,
                                                             category))
            break
        except ValueError:
            print("Invalid input. ")
    it.commit()


def track_income():
    """Track the total income for all the category and print the total amount
    and the current category in the database.
    """
    cursor_it.execute('SELECT income_category FROM income_tracking ')
    income_category = [row[0] for row in cursor_it.fetchall()]
    print("Current income category in the database. ")
    print(income_category)
    cursor_it.execute('SELECT income FROM income_tracking')
    incomes = [int(row[0]) for row in cursor_it.fetchall()]
    total = 0
    for income in incomes:
        total = total + income
    print(f"The total spending is {total}.")


# # view expense or income categories
# def view_categories():
#     """View both expense and income categories
#     """
#     cursor_et.execute('SELECT * FROM expense_tracking')
#     expense_view = [row for row in cursor_et.fetchall()]
#     cursor_it.execute('SELECT * FROM income_tracking')
#     income_view = [row for row in cursor_it.fetchall()]
#     print(f"{expense_view}\n{income_view}")


# view expense by categories
def view_expense_category():
    """
    View expense by category, prompt the user if they want to update, delete
    categories or go back to the main menu. If there are no more categories
    left it will put the user back to the main menu.
    """
    cursor_et.execute('SELECT expense_category FROM expense_tracking ')
    expense_categories = [row[0] for row in cursor_et.fetchall()]
    while True:
        category = input(
            """Which category do you want to view?
* Type exit to go back to the menu.
""").capitalize()
        if category in expense_categories:
            cursor_et.execute('''SELECT expense_category, expense
                            FROM expense_tracking
                            WHERE expense_category=?''', (category,))
            expense_view = [cursor_et.fetchone()]
            for expense_category, expense in expense_view:
                print('_' * 50)
                print(f"""Category: {expense_category}
Current Expense: {expense}""")
                print('_' * 50)
            time.sleep(1)
            status = input("Update expense, delete category or exit? "
                           ).capitalize()
            if status == 'Delete':
                delete_choice = input(
                    "Would you like to delete this category? (Y/N) "
                    ).capitalize()
                if delete_choice == "Y":
                    cursor_et.execute('''DELETE FROM expense_tracking WHERE
                            expense_category=?''', (category,))
                    expense_categories.remove(category)
            elif status == "Update":
                expense_amount(category)
            elif status == "Exit":
                print("Exiting to main menu. ")
                break
            time.sleep(1)
            if expense_categories:
                choice = input(
                    "Would you like to view another expense? (Y/N) "
                    ).capitalize()
                if choice == "Y":
                    continue
                elif choice == "N":
                    print("Exiting to main menu. ")
                    break
            elif not expense_categories:
                print("There are no more categories")
                time.sleep(1)
                print("Exiting to main menu. ")
                break
        elif category == "Exit":
            print("Exiting to main menu. ")
            break
        else:
            print("Category not found. Please try again. ")
    et.commit()


def view_income_category():
    """
    View income by category, prompt the user if they want to update, delete
    categories or go back to the main menu. If there are no more categories
    left it will put the user back to the main menu.
    """
    cursor_it.execute('SELECT income_category FROM income_tracking ')
    income_categories = [row[0] for row in cursor_it.fetchall()]
    while True:
        category = input(
            """Which category do you want to view?
* Type exit to go back to the menu.
""").capitalize()
        if category in income_categories:
            cursor_it.execute('''SELECT income_category, income
                            FROM income_tracking
                            WHERE income_category=?''', (category,))
            income_view = [cursor_it.fetchone()]
            for income_category, income in income_view:
                print('_' * 50)
                print(f"""Category: {income_category}
Current Income: {income}""")
                print('_' * 50)
            time.sleep(1)
            status = input("Update income, delete category or exit? "
                           ).capitalize()
            if status == 'Delete':
                delete_choice = input(
                    "Would you like to delete this category? (Y/N) "
                    ).capitalize()
                if delete_choice == "Y":
                    cursor_it.execute('''DELETE FROM income_tracking WHERE
                            income_category=?''', (category,))
                    income_categories.remove(category)
            elif status == "Update":
                income_amount(category)
            elif status == "Exit":
                print("Exiting to main menu. ")
                break
            time.sleep(1)
            if income_categories:
                choice = input(
                    "Would you like to view another income? (Y/N) "
                    ).capitalize()
                if choice == "Y":
                    continue
                elif choice == "N":
                    print("Exiting to main menu. ")
                    break
            elif not income_categories:
                print("There are no more categories")
                time.sleep(1)
                print("Exiting to main menu. ")
                break
        elif category == "Exit":
            print("Exiting to main menu. ")
            break
        else:
            print("Category not found. Please try again. ")
    it.commit()


def budget_amount(category):
    """Update the budget table for the given category.

    Args:
        category (str): The current category being viewed.
    """
    while True:
        budget_amount = input("Please enter your budget amount. ")
        cursor_bt.execute('''UPDATE budget_tracking SET budget=?
                            WHERE budget_category=?''', (budget_amount,
                                                         category))
        break
    bt.commit()


def set_budget():
    """
    Let the user set the budget amount for a given category.
    Give the user the option to return to the main menu.
    Another prompt to set another category is given to the user after the
    first one.
    """
    while True:
        cursor_bt.execute('SELECT budget_category FROM budget_tracking')
        budget_category = [row[0] for row in cursor_bt.fetchall()]
        user_category = input(
            """Please enter the name of the category you want to add.
* Type exit to go back to the menu.
""").capitalize()
        if user_category in budget_category:
            print("Category already in the database. ")
        elif user_category == 'Exit':
            print("Exiting to the main menu. ")
            break
        else:
            while True:
                try:
                    user_budget = int(input("Please enter the budget "))
                    cursor_bt.execute('''INSERT INTO budget_tracking(
                    budget_category, budget)
                    VALUES(?,?)''', (user_category, user_budget))
                    break
                except ValueError:
                    print("Invalid input. ")
            choice = input(
                    "Would you like to set another category? (Y/N) "
                    ).capitalize()
            if choice == "Y":
                continue
            elif choice == "N":
                print("Exiting to main menu. ")
                break


def view_budget():
    """
    View income by category, prompt the user if they want to update, delete
    categories or go back to the main menu. If there are no more categories
    left it will put the user back to the main menu.
    """
    cursor_bt.execute('SELECT budget_category FROM budget_tracking ')
    budget_categories = [row[0] for row in cursor_bt.fetchall()]
    while True:
        category = input(
            """Which category do you want to view?
* Type exit to go back to the menu.
""").capitalize()
        if category in budget_categories:
            cursor_bt.execute('''SELECT budget_category, budget
                            FROM budget_tracking
                            WHERE budget_category=?''', (category,))
            budget_view = [cursor_bt.fetchone()]
            for budget_category, budget in budget_view:
                print('_' * 50)
                print(f"""Category: {budget_category}
Current Budget: {budget}""")
                print('_' * 50)
            time.sleep(1)
            status = input("Update budget, delete category or exit? "
                           ).capitalize()
            if status == 'Delete':
                delete_choice = input(
                    "Would you like to delete this category? (Y/N) "
                    ).capitalize()
                if delete_choice == "Y":
                    cursor_bt.execute('''DELETE FROM budget_tracking WHERE
                            budget_category=?''', (category,))
                    budget_categories.remove(category)
            elif status == "Update":
                budget_amount(category)
            elif status == "Exit":
                print("Exiting to main menu. ")
                break
            time.sleep(1)
            if budget_categories:
                choice = input(
                    "Would you like to view another budget? (Y/N) "
                    ).capitalize()
                if choice == "Y":
                    continue
                elif choice == "N":
                    print("Exiting to main menu. ")
                    break
            elif not budget_categories:
                print("There are no more categories")
                time.sleep(1)
                print("Exiting to main menu. ")
                break
        elif category == "Exit":
            print("Exiting to main menu. ")
            break
        else:
            print("Category not found. Please try again. ")
    bt.commit()


def financial_goals():
    """
    Set a financial goal for the user.
    """
    while True:
        goal = input(
                """What is your financial goals?
* Type exit to go back to the menu.
""")
        if goal == 'exit':
            print("Exiting to the main menu. ")
            break
        else:
            print(f"Your financial goal is {goal}.")
            try:
                return int(goal)
            except ValueError:
                print("Please enter a numerical value. ")


def goal_progress(goal):
    """
    Allow the user to check how far they are from the goal with their current
    expense and income.
    """
    cursor_it.execute('SELECT income FROM income_tracking')
    incomes = [int(row[0]) for row in cursor_it.fetchall()]
    income_total = 0
    for income in incomes:
        income_total = income_total + income
    cursor_et.execute('SELECT expense FROM expense_tracking')
    expenses = [int(row[0]) for row in cursor_et.fetchall()]
    expense_total = 0
    for expense in expenses:
        expense_total = expense_total + expense
    saving = income_total - expense_total
    goal_progress = goal - saving
    print(f"Current saving is {saving}\n"
          f"You are still {goal_progress} away from your goal.")


# set up of sqlite3 for all 3 database
bt = sqlite3.connect('L3T08/budget_tracking.db')
cursor_bt = bt.cursor()
et = sqlite3.connect('L3T08/expense_tracking.db')
cursor_et = et.cursor()
it = sqlite3.connect('L3T08/income_tracking.db')
cursor_it = it.cursor()


# main block of code for the menu
try:
    goal = 0
    cursor_bt.execute('''CREATE TABLE IF NOT EXISTS budget_tracking(
        id INTEGER PRIMARY KEY,
        budget_category TEXT,
        budget INTEGER
    )''')
    default_bt = [(1, "General", 0)]
    cursor_bt.executemany('''INSERT OR IGNORE INTO budget_tracking
                    (id, budget_category, budget)
                    VALUES (?,?,?)''', default_bt)
    bt.commit()

    cursor_et.execute('''CREATE TABLE IF NOT EXISTS expense_tracking(
            id INTEGER PRIMARY KEY,
            expense_category TEXT,
            expense INTEGER
    )''')
    default_et = [(1, "General", 0)]
    cursor_et.executemany('''INSERT OR IGNORE INTO expense_tracking
                        (id, expense_category, expense)
                        VALUES (?,?,?)''', default_et)
    et.commit()

    cursor_it.execute('''CREATE TABLE IF NOT EXISTS income_tracking(
            id INTEGER PRIMARY KEY,
            income_category TEXT,
            income INTEGER
    )''')
    default_it = [(1, "General", 0)]
    cursor_it.executemany('''INSERT OR IGNORE INTO income_tracking
                        (id, income_category, income)
                        VALUES (?,?,?)''', default_it)
    it.commit()
    while True:
        print("""______________________________________________
        1. Add expense
        2. View expenses
        3. View expenses by category
        4. Add income
        5. View income
        6. View income by category
        7. Set budget for a category
        8. view budget for a category
        9. Set financial goals
        10. View progress towards financial goals
        11. Quit
______________________________________________""")

        user_choice = input("What would you like to do? ")
        if user_choice == "1":
            new_expenses()
            time.sleep(1)
        elif user_choice == "2":
            track_spending()
            time.sleep(1)
        elif user_choice == "3":
            view_expense_category()
            time.sleep(1)
        elif user_choice == "4":
            new_income()
            time.sleep(1)
        elif user_choice == "5":
            track_income()
            time.sleep(1)
        elif user_choice == "6":
            view_income_category()
            time.sleep(1)
        elif user_choice == "7":
            set_budget()
            time.sleep(1)
        elif user_choice == "8":
            view_budget()
            time.sleep(1)
        elif user_choice == "9":
            goal = financial_goals()
            time.sleep(1)
        elif user_choice == "10":
            # prompt the user to use option 9 if they have not set a goal
            if not goal:
                print("Please use the function 9 "
                      "to create a financial goal first.")
            else:
                goal_progress(goal)
            time.sleep(1)
        elif user_choice == "11":
            print("Exiting programme. ")
            break
        else:
            print("Invalid input. ")

except Exception as e:
    bt.rollback()
    et.rollback()
    it.rollback()
    raise e
finally:
    bt.close()
    et.close()
    it.close()
