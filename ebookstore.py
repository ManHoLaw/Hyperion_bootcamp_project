import sqlite3
import time
import re

# dictionary holding the input prompts
prompts = {
        "id": "Please enter the id of the book: ",
        "title": "Please enter the title of the book: ",
        "author": "Please enter the author of the book: ",
        "qty": "Please enter the quantity of the book: ",
    }
# dictionary to hold the data type for each column
data_type = {
        "id": int,
        "title": str,
        "author": str,
        "qty": int,
    }
# dictionary to hold the book information
book_data = {}
book_id = []


def user_action(action):
    cursor.execute("SELECT id FROM book")
    print("Current book in the database: ")
    for row in cursor.fetchall():
        book_id.append(row[0])
    print(book_id)
    if action == 1:
        print('Add Book')
        add_book()
    elif action == 2:
        print('Updating Book')
        update_book()
    elif action == 3:
        print('Delete Book')
        delete_book()
    elif action == 4:
        print('Search Book')
        search_book()
    book_id.clear()
    db.commit()
    return


# Add a book to the database
def add_book():
    # Fill the book_data with user input to add to the table
    for field, prompt in prompts.items():
        while True:
            try:
                user_input = input(prompt)
                book_data[field] = data_type[field](user_input)
                if field == 'id':
                    if get_id(book_data['id']) == 0:
                        break
                    else:
                        print("The ID is already in the database. ")
                if field == 'title' or field == 'author':
                    book_data[field] = book_data[field].title()
                    break
                if field == 'author':
                    if re.search(r'[0-9]', book_data['author']):
                        print("Invalid Author name. ")
                    else:
                        break
                if field == 'qty':
                    break
            except ValueError:
                print("Invalid Input. Please try again.")
    cursor.execute('''INSERT OR IGNORE INTO book(id, title, author, qty)
                VALUES(?,?,?,?)''', (book_data['id'], book_data['title'],
                                     book_data['author'], book_data['qty']))
    for field, data in book_data.items():
        if field == 'qty':
            field = 'quantity'
        print(f"{field.capitalize()}: {data}")
    time.sleep(1)


# Find the id of the book that needs to be updated with user input.
def update_book():
    while (id := get_id()) == -1:
        pass
    while True:
        update_field = input(
            '''Please enter the information you want to update.
You can enter multiple separated with a comma.
(e.g., title, author, quantity):\n''').strip().lower()
        fields_to_update = [field.strip()
                            for field in update_field.split(',')]
        fields_to_update = ["qty" if field == "quantity"
                            else field for field in fields_to_update]
        invalid_fields = [field for field in fields_to_update
                          if field not in prompts]
        if invalid_fields:
            print(f"Invalid fields: {invalid_fields}")
        else:
            break
    for field, prompt in prompts.items():
        try:
            if field in fields_to_update:
                user_input = input(prompt)
                book_data[field] = data_type[field](user_input)
                if field == 'title' or field == 'author':
                    book_data[field] = book_data[field].title()
                cursor.execute(f'''UPDATE book SET {field}=? WHERE id=?''',
                               (book_data[field], id))
                print('Book updated. ')
        except ValueError:
            print("Invalid input. Please try again.")


# Delete an entry from the database for the given id
def delete_book():
    while (id := get_id()) == -1:
        pass
    confirm = input('''Are you sure you want to delete this book?
Yes: 1
No: 0
''')
    while True:
        if confirm:
            cursor.execute('SELECT * FROM book WHERE id=?', (id,))
            book_searched = cursor.fetchone()
            cursor.execute('DELETE FROM book WHERE id=?''', (id,))
            print(f"Successfully deleted book: {book_searched[1]}")
            break
        elif not confirm:
            return
        else:
            print("Invalid Input.")


# search the entry with the id in the database
def search_book():
    while (id := get_id()) == -1:
        pass
    cursor.execute('SELECT * FROM book WHERE id=?', (id,))
    book_searched = cursor.fetchone()
    for field, data in zip(prompts.keys(), book_searched):
        if field == 'qty':
            field = 'quantity'
        print(f"{field.capitalize()}: {data}")
    time.sleep(1)


# Get user input for id and check if the id of the book exist in the database
def get_id(input_id=0):
    attempt = 0
    while True:
        try:
            if not input_id:
                input_id = int(input('Please input the ID of the book. '))
                attempt = 1
        except ValueError:
            print("Invalid Input. Please try again.")
            continue
        cursor.execute('''SELECT COUNT(*) FROM book WHERE id=?''', (input_id,))
        count = cursor.fetchone()[0]
        if count:
            break
        elif not count and attempt == 0:
            return 0
        else:
            print("Book ID is not in the database.")
            return -1
    return input_id


file_path = 'L2T07/ebookstore.db'
db = sqlite3.connect(file_path)
cursor = db.cursor()
try:
    print("Connected to the existing database.")
    cursor.execute('''CREATE TABLE IF NOT EXISTS book(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INTEGER NOT NULL)''')

    default_books = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                     (3002, "Harry Potter and the Philosopher's Stone",
                      'J.K. Rowling', 40),
                     (3003, 'The Lion, the Witch and the Wardrobe',
                      'C.S, Lewis', 25),
                     (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                     (3005, 'Alice in the Wonderland', 'Lewis Carroll', 12)]

    cursor.executemany('''INSERT OR IGNORE INTO book(
        id, title, author, qty) VALUES(?,?,?,?)''', default_books)
    db.commit()

    while True:
        print("_" * 50)
        print('''1. Enter book
2. Update book
3. Delete book
4. Search book
0. Exit''')
        try:
            action = int(
                input("Please enter the number correspond to the action. "))
        except ValueError:
            print("Please enter a number corresponding to your action. ")
            time.sleep(2)
            continue
        if action == 0:
            print("Exiting database. ")
            time.sleep(1)
            break
        elif action in range(1, 5):
            user_action(action)
        else:
            print("Invalid action. ")
            time.sleep(1)

except Exception as e:
    db.rollback()
    raise e
finally:
    db.close()
