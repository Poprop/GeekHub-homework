import sqlite3


class AdminATM:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.current_user = None
        self.bill_inventory = {10: 0, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}

    def admin_login(self, admin_name, admin_password):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""SELECT id FROM users WHERE name=? AND password=?""", (admin_name, admin_password))
            result = cur.fetchone()
            if result and admin_name == "Admin" and admin_password.lower() == "admin":
                self.current_user = result[0]
                print("Hello Administrator, you've entered into admin panel")
                self.admin_menu()
            else:
                print("You entered an invalid login or password")

    def admin_menu(self):
        while self.current_user:
            menu_options = {
                '1': 'check_total_bank_balance',
                '2': 'deposit_bills',
                '3': 'admin_logout'
            }
            print("ATM menu, choose one of these actions by entering a number: ")
            for key, value in menu_options.items():
                print(f"{key} <-------- {value}")
            choice = input("Your choice is: ")
            if choice in menu_options:
                getattr(self, menu_options[choice])()
            else:
                print("Invalid option, try again")
            if not self.current_user:
                break

    def check_total_bank_balance(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""SELECT * FROM bills_inventory""")
            rows = cur.fetchall()
            total = sum(row[1] * row[2] for row in rows)
            for row in rows:
                print(f"In ATM there are {row[1]} ----> {row[2]} bills")
                print(f"The total amount of money in the ATM - {total}")
            return total

    def check_total_bank_for_user_funks(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""SELECT * FROM bills_inventory""")
            rows = cur.fetchall()
            total = sum(row[1] * row[2] for row in rows)
            return total

    def update_bill_inventory(self, amount):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""SELECT * FROM bills_inventory""")
            rows = cur.fetchall()

            # Convert the rows to a dictionary for easier manipulation
            current_inventory = {row[0]: row[2] for row in rows}

            for bill in sorted(self.bill_inventory.keys(), reverse=True):
                while amount >= bill:
                    self.bill_inventory[bill] += 1
                    current_inventory.setdefault(bill, 0)
                    current_inventory[bill] += 1
                    amount -= bill

            update_values = [(quantity, nominal) for nominal, quantity in current_inventory.items()]

            cur.executemany("""
                UPDATE bills_inventory
                SET quantity = ?
                WHERE nominal = ?
            """, update_values)

            self.conn.commit()

    def deposit_bills(self):
        print("You enter the bills deposit menu, enter the amount of bills you want to add: ")
        while True:
            try:
                denomination = int(input("Enter the denomination: "))
                num_of_bills = int(input(f"Enter the amount of {denomination} bills: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("""UPDATE bills_inventory SET quantity = quantity + ? WHERE nominal = ?""",
                        (num_of_bills, denomination))

    def admin_logout(self):
        self.current_user = None
        print("You have logged out from the system")
