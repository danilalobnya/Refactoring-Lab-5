import sqlite3

'''
A program to create and use a database called 'ebookstore.db' with a table
called 'book'. This database is for a bookstore and allows the clerk to;
log, update, delete, search for and view books in the store as well as provide
quantity's of each book.
'''


# Function to create the 'book' table in the database
def create_table():
    conn = sqlite3.connect('ebookstore.db')  # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                qty INTEGER
            )
        ''') # Execute SQL query to create the 'book' table if it doesn't exist

        conn.commit() # Commit the transaction
    except sqlite3.Error as e:
        print(f"Error creating table: {e}") # Print error message if an error occurs
    finally:
        conn.close() # Close the database connection


# Function to insert initial data into the 'book' table
def insert_initial_data():
    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

    try:
        cursor.execute('SELECT COUNT(*) FROM book')  # Execute SQL query to count existing records
        existing_records = cursor.fetchone()[0] # Fetch the count of existing records

        if existing_records == 0:
            # Insert initial data into the 'book' table if it's empty
            cursor.executemany('''
                INSERT INTO book (id, title, author, genre, qty) VALUES (?, ?, ?, ?, ?)
            ''', [
                (3001, 'A Tale of Two Cities', 'Charles Dickens', 'Fiction', 30),
                (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 'Fantasy', 40),
                (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 'Fantasy', 25),
                (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 37),
                (3005, 'Alice in Wonderland', 'Lewis Carroll', 'Fantasy', 12),
            ])

            conn.commit()  # Commit the transaction
    except sqlite3.Error as e:
        print(f"Error inserting initial data: {e}")  # Print error message if an error occurs
    finally:
        conn.close()  # Close the database connection


def create_indexes():
    conn = sqlite3.connect('ebookstore.db')
    cursor = conn.cursor()

    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_title ON book(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_author ON book(author)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_genre ON book(genre)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_book_qty ON book(qty)')

        conn.commit()
        print("Indexes created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating indexes: {e}")
    finally:
        conn.close()


# Capture a new book
def enter_book():
    try:
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        genre = input("Enter book genre: ")
        qty = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid input. Quantity must be a valid integer.")
        return

    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor()# Create a cursor object to execute SQL queries

    try:
        cursor.execute('''
            INSERT INTO book (title, author, genre, qty) VALUES (?, ?, ?, ?)
        ''', (title, author, genre, qty))

        book_id = cursor.lastrowid

        conn.commit() # Commit the transaction
        print(f"The book has been added to inventory. The ID has been assigned to {book_id}.")
    except sqlite3.Error as e:
        print(f"Error entering book: {e}") # Print error message if an error occurs
    finally:
        conn.close() # Close the database connection


# Function to update or edit book details using the book ID number
def update_book():
    try:
        book_id = int(input("Enter book ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for book ID.")
        return

    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor()# Create a cursor object to execute SQL queries

    try:
        # необходимые поля вместо SELECT *
        cursor.execute('SELECT title, author, genre, qty FROM book WHERE id = ?', (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book ID not found. Please enter a valid book ID.")
            return

        current_title, current_author, current_genre, current_qty = book

        print("\nCurrent Book Details:")
        print(f"Title: {current_title}")
        print(f"Author: {current_author}")
        print(f"Genre: {current_genre}")
        print(f"Quantity: {current_qty}\n")

        updates = []
        params = []

        new_title = input("Enter new title (leave blank to keep current): ").strip()
        if new_title:
            updates.append("title = ?")
            params.append(new_title)
        else:
            params.append(current_title)

        new_author = input("Enter new author (leave blank to keep current): ").strip()
        if new_author:
            updates.append("author = ?")
            params.append(new_author)
        else:
            params.append(current_author)

        new_genre = input("Enter new genre (leave blank to keep current): ").strip()
        if new_genre:
            updates.append("genre = ?")
            params.append(new_genre)
        else:
            params.append(current_genre)

        new_qty = input("Enter new quantity (leave blank to keep current): ").strip()
        if new_qty:
            try:
                new_qty = int(new_qty)
                updates.append("qty = ?")
                params.append(new_qty)
            except ValueError:
                print("Invalid quantity - keeping current value")
                params.append(current_qty)
        else:
            params.append(current_qty)

        # обновляем только измененные поля
        if updates:
            update_query = f"UPDATE book SET {', '.join(updates)} WHERE id = ?"
            params.append(book_id)

            cursor.execute(update_query, params)
            conn.commit()
            print("Book details updated successfully.")
        else:
            print("No changes detected - book not updated.")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error updating book: {e}")
    finally:
        conn.close()


# Function to delete a book with the book ID
def delete_book():
    try:
        book_id = int(input("Enter book ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for book ID.")
        return

    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

    try:
        # необходимые поля вместо SELECT *
        cursor.execute('SELECT id, title FROM book WHERE id = ?', (book_id,))
        book = cursor.fetchone()

        if not book:
            print("Book ID not found. Please enter a valid book ID.")
            return

        book_id, book_title = book
        print(f"\nBook to delete: {book_title} (ID: {book_id})\n")

        while True:
            confirm = input("Are you sure you want to delete this book? (yes/no): ").lower()
            if confirm in ('yes', 'no'):
                break
            print("Please enter 'yes' or 'no'")

        if confirm == 'yes':
            cursor.execute('DELETE FROM book WHERE id = ?', (book_id,))
            conn.commit()
            print("Book deleted successfully.")
        else:
            print("Deletion canceled.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error deleting book: {e}")
    finally:
        conn.close()

# Function to search all the books by either the title/author/genre
def search_books():
    keyword = input("Enter search keyword (title/author/genre): ").casefold()

    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

    try:
        # конкретные поля вместо SELECT *
        cursor.execute('''
            SELECT id, title, author, genre, qty 
            FROM book 
            WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
            ORDER BY title
        ''', ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

        books = cursor.fetchall()

        if books:
            for book in books:
                print(book)
        else:
            print("No books found.")
    except sqlite3.Error as e:
        handle_search_error(e)
    finally:
        conn.close()


# Function to view all the books and their corresponding ID numbers
def view_all_books():
    conn = sqlite3.connect('ebookstore.db') # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL queries

    try:
        # конкретные поля
        cursor.execute('''
            SELECT id, title, author, genre, qty 
            FROM book 
            ORDER BY title
        ''')

        books = cursor.fetchall()

        if books:
            for book in books:
                print(book)
        else:
            print("No books found.")
    except sqlite3.Error as e:
        handle_view_all_error(e)
    finally:
        conn.close()


def analyze_original_search():
    conn = sqlite3.connect('ebookstore.db')
    cursor = conn.cursor()

    print("Анализ оригинального запроса поиска:")
    cursor.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM book WHERE title LIKE '%harry%' OR author LIKE '%harry%' OR genre LIKE '%harry%'")

    for row in cursor:
        print(row)

    conn.close()


def analyze_optimized_search():
    conn = sqlite3.connect('ebookstore.db')
    cursor = conn.cursor()

    print("\nАнализ оптимизированного запроса поиска:")
    cursor.execute(
        "EXPLAIN QUERY PLAN SELECT id, title, author, genre, qty FROM book WHERE title LIKE '%harry%' OR author LIKE '%harry%' OR genre LIKE '%harry%' ORDER BY title")

    for row in cursor:
        print(row)

    conn.close()


#Added 5 new functions for additional error handling
# Function to handle invalid inputs when entering a new book
def handle_invalid_input():
    print("Invalid input. Please enter a valid integer.")

# Function to handle errors when updating book details
def handle_update_error(e):
    print(f"Error updating book: {e}")

# Function to handle errors when deleting a book
def handle_delete_error(e):
    print(f"Error deleting book: {e}")

# Function to handle errors when searching for books
def handle_search_error(e):
    print(f"Error searching books: {e}")

# Function to handle errors when viewing all books
def handle_view_all_error(e):
    print(f"Error viewing all books: {e}")


# Main program
if __name__ == "__main__":
    create_table()
    insert_initial_data()

    while True:
        print("\nMenu:")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View all books")
        print("6. Analyze original search")
        print("7. Analyze optimized search")
        print("0. Exit")

        choice = input("Enter your choice: ")
        print("")

        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            view_all_books()
        elif choice == '6':
            analyze_original_search()
        elif choice == '7':
            analyze_optimized_search()
        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
        else:
            # Print error message if an error occurs
            print("Invalid choice. Please try again.")
