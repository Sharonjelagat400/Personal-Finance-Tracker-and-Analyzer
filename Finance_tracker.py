import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    category TEXT,
                    amount REAL,
                    date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )''')

# Function to register a new user
def register(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

# Function to log in a user
def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Welcome back, {username}!")
        return user[0]  # Return the user_id
    else:
        print("Invalid username or password. Please try again.")
        return None

# Function to record a transaction
def record_transaction(user_id, category, amount, date):
    cursor.execute("INSERT INTO transactions (user_id, category, amount, date) VALUES (?, ?, ?, ?)",
                   (user_id, category, amount, date))
    conn.commit()
    print("Transaction recorded successfully!")

# Function to generate a summary of transactions
def generate_summary(user_id):
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id=? GROUP BY category", (user_id,))
    summary = cursor.fetchall()
    df = pd.DataFrame(summary, columns=['Category', 'Total Amount'])
    print(df)

    # Generate a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(df['Total Amount'], labels=df['Category'], autopct='%1.1f%%')
    plt.title('Expense Distribution')
    plt.show()

# Main function
def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Record Transaction")
        print("4. Generate Summary")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = login(username, password)
            if user_id:
                while True:
                    print("\n1. Record Transaction")
                    print("2. Generate Summary")
                    print("3. Logout")
                    inner_choice = input("Enter your choice: ")
                    if inner_choice == '1':
                        category = input("Enter category: ")
                        amount = float(input("Enter amount: "))
                        date = input("Enter date (YYYY-MM-DD): ")
                        record_transaction(user_id, category, amount, date)
                    elif inner_choice == '2':
                        generate_summary(user_id)
                    elif inner_choice == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
