import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import csv
from datetime import datetime

class CommunityApp:
    def __init__(self, master):
        self.master = master
        master.title("Community Empowerment Project")
        self.init_database()
        self.create_widgets()

    def init_database(self):
        try:
            self.conn = sqlite3.connect("community.db")
            self.cursor = self.conn.cursor()
            self.create_tables()
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                address TEXT,
                contact_info TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS parcels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL UNIQUE,
                size TEXT,
                location TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS allocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                parcel_id INTEGER NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members (id),
                FOREIGN KEY (parcel_id) REFERENCES parcels (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                payment_method TEXT,
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Create frames
        self.member_frame = tk.Frame(self.master)
        self.member_frame.pack(pady=10)

        self.land_frame = tk.Frame(self.master)
        self.land_frame.pack(pady=10)

        self.contribution_frame = tk.Frame(self.master)
        self.contribution_frame.pack(pady=10)

        self.expense_frame = tk.Frame(self.master)
        self.expense_frame.pack(pady=10)

        self.allocation_frame = tk.Frame(self.master)
        self.allocation_frame.pack(pady=10)

        # Member Information
        tk.Label(self.member_frame, text="Member Name:").grid(row=0, column=0, sticky='e')
        self.member_name_entry = tk.Entry(self.member_frame)
        self.member_name_entry.grid(row=0, column=1)

        tk.Label(self.member_frame, text="Address:").grid(row=1, column=0, sticky='e')
        self.member_address_entry = tk.Entry(self.member_frame)
        self.member_address_entry.grid(row=1, column=1)

        tk.Label(self.member_frame, text="Contact Info:").grid(row=2, column=0, sticky='e')
        self.member_contact_entry = tk.Entry(self.member_frame)
        self.member_contact_entry.grid(row=2, column=1)

        tk.Button(self.member_frame, text="Add Member", command=self.add_member).grid(row=3, column=0, columnspan=2, pady=5)

        # Land Information
        tk.Label(self.land_frame, text="Parcel Number:").grid(row=0, column=0, sticky='e')
        self.parcel_number_entry = tk.Entry(self.land_frame)
        self.parcel_number_entry.grid(row=0, column=1)

        tk.Label(self.land_frame, text="Size:").grid(row=1, column=0, sticky='e')
        self.parcel_size_entry = tk.Entry(self.land_frame)
        self.parcel_size_entry.grid(row=1, column=1)

        tk.Label(self.land_frame, text="Location:").grid(row=2, column=0, sticky='e')
        self.parcel_location_entry = tk.Entry(self.land_frame)
        self.parcel_location_entry.grid(row=2, column=1)

        tk.Button(self.land_frame, text="Add Parcel", command=self.add_parcel).grid(row=3, column=0, columnspan=2, pady=5)

        # Allocation
        tk.Label(self.allocation_frame, text="Allocate Member to Parcel").grid(row=0, column=0, columnspan=2)
        tk.Label(self.allocation_frame, text="Member Name:").grid(row=1, column=0, sticky='e')
        self.allocate_member_name_entry = tk.Entry(self.allocation_frame)
        self.allocate_member_name_entry.grid(row=1, column=1)

        tk.Label(self.allocation_frame, text="Parcel Number:").grid(row=2, column=0, sticky='e')
        self.allocate_parcel_number_entry = tk.Entry(self.allocation_frame)
        self.allocate_parcel_number_entry.grid(row=2, column=1)

        tk.Button(self.allocation_frame, text="Allocate", command=self.allocate_member).grid(row=3, column=0, columnspan=2, pady=5)

        # Contribution Tracking
        tk.Label(self.contribution_frame, text="Member Name:").grid(row=0, column=0, sticky='e')
        self.contribution_member_entry = tk.Entry(self.contribution_frame)
        self.contribution_member_entry.grid(row=0, column=1)

        tk.Label(self.contribution_frame, text="Amount:").grid(row=1, column=0, sticky='e')
        self.contribution_amount_entry = tk.Entry(self.contribution_frame)
        self.contribution_amount_entry.grid(row=1, column=1)

        tk.Label(self.contribution_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.contribution_date_entry = tk.Entry(self.contribution_frame)
        self.contribution_date_entry.grid(row=2, column=1)

        tk.Label(self.contribution_frame, text="Payment Method:").grid(row=3, column=0, sticky='e')
        self.contribution_method_entry = tk.Entry(self.contribution_frame)
        self.contribution_method_entry.grid(row=3, column=1)

        tk.Button(self.contribution_frame, text="Record Contribution", command=self.record_contribution).grid(row=4, column=0, columnspan=2, pady=5)

        # Expense Tracking
        tk.Label(self.expense_frame, text="Description:").grid(row=0, column=0, sticky='e')
        self.expense_description_entry = tk.Entry(self.expense_frame)
        self.expense_description_entry.grid(row=0, column=1)

        tk.Label(self.expense_frame, text="Amount:").grid(row=1, column=0, sticky='e')
        self.expense_amount_entry = tk.Entry(self.expense_frame)
        self.expense_amount_entry.grid(row=1, column=1)

        tk.Label(self.expense_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.expense_date_entry = tk.Entry(self.expense_frame)
        self.expense_date_entry.grid(row=2, column=1)

        tk.Label(self.expense_frame, text="Category:").grid(row=3, column=0, sticky='e')
        self.expense_category_entry = tk.Entry(self.expense_frame)
        self.expense_category_entry.grid(row=3, column=1)

        tk.Button(self.expense_frame, text="Record Expense", command=self.record_expense).grid(row=4, column=0, columnspan=2, pady=5)

        # Export Data Button
        tk.Button(self.master, text="Export Data to CSV", command=self.export_data).pack(pady=10)

    def add_member(self):
        name = self.member_name_entry.get()
        address = self.member_address_entry.get()
        contact = self.member_contact_entry.get()

        if name:
            try:
                self.cursor.execute("INSERT INTO members (name, address, contact_info) VALUES (?, ?, ?)",
                                    (name, address, contact))
                self.conn.commit()
                messagebox.showinfo("Success", f"Member '{name}' added successfully.")
                self.member_name_entry.delete(0, tk.END)
                self.member_address_entry.delete(0, tk.END)
                self.member_contact_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"Member '{name}' already exists.")
        else:
            messagebox.showerror("Error", "Member name is required.")

    def add_parcel(self):
        number = self.parcel_number_entry.get()
        size = self.parcel_size_entry.get()
        location = self.parcel_location_entry.get()

        if number:
            try:
                self.cursor.execute("INSERT INTO parcels (number, size, location) VALUES (?, ?, ?)",
                                    (number, size, location))
                self.conn.commit()
                messagebox.showinfo("Success", f"Parcel '{number}' added successfully.")
                self.parcel_number_entry.delete(0, tk.END)
                self.parcel_size_entry.delete(0, tk.END)
                self.parcel_location_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"Parcel '{number}' already exists.")
        else:
            messagebox.showerror("Error", "Parcel number is required.")

    def allocate_member(self):
        member_name = self.allocate_member_name_entry.get()
        parcel_number = self.allocate_parcel_number_entry.get()

        if member_name and parcel_number:
            # Find member_id
            self.cursor.execute("SELECT id FROM members WHERE name = ?", (member_name,))
            member = self.cursor.fetchone()

            # Find parcel_id
            self.cursor.execute("SELECT id FROM parcels WHERE number = ?", (parcel_number,))
            parcel = self.cursor.fetchone()

            if member and parcel:
                try:
                    self.cursor.execute("INSERT INTO allocations (member_id, parcel_id) VALUES (?, ?)",
                                        (member[0], parcel[0]))
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Member '{member_name}' allocated to parcel '{parcel_number}'.")
                    self.allocate_member_name_entry.delete(0, tk.END)
                    self.allocate_parcel_number_entry.delete(0, tk.END)
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "This allocation already exists.")
            else:
                messagebox.showerror("Error", "Member or Parcel not found.")
        else:
            messagebox.showerror("Error", "Member name and Parcel number are required.")

    def record_contribution(self):
        member_name = self.contribution_member_entry.get()
        amount = self.contribution_amount_entry.get()
        date = self.contribution_date_entry.get()
        payment_method = self.contribution_method_entry.get()

        if member_name and amount and date:
            # Validate date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            # Find member_id
            self.cursor.execute("SELECT id FROM members WHERE name = ?", (member_name,))
            member = self.cursor.fetchone()

            if member:
                try:
                    self.cursor.execute("""
                        INSERT INTO contributions (member_id, amount, date, payment_method)
                        VALUES (?, ?, ?, ?)
                    """, (member[0], float(amount), date, payment_method))
                    self.conn.commit()
                    messagebox.showinfo("Success", f"Contribution recorded for member '{member_name}'.")
                    self.contribution_member_entry.delete(0, tk.END)
                    self.contribution_amount_entry.delete(0, tk.END)
                    self.contribution_date_entry.delete(0, tk.END)
                    self.contribution_method_entry.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount.")
            else:
                messagebox.showerror("Error", f"Member '{member_name}' not found.")
        else:
            messagebox.showerror("Error", "Member name, amount, and date are required.")

    def record_expense(self):
        description = self.expense_description_entry.get()
        amount = self.expense_amount_entry.get()
        date = self.expense_date_entry.get()
        category = self.expense_category_entry.get()

        if description and amount and date:
            # Validate date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                self.cursor.execute("""
                    INSERT INTO expenses (description, amount, date, category)
                    VALUES (?, ?, ?, ?)
                """, (description, float(amount), date, category))
                self.conn.commit()
                messagebox.showinfo("Success", "Expense recorded successfully.")
                self.expense_description_entry.delete(0, tk.END)
                self.expense_amount_entry.delete(0, tk.END)
                self.expense_date_entry.delete(0, tk.END)
                self.expense_category_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")
        else:
            messagebox.showerror("Error", "Description, amount, and date are required.")

    def export_data(self):
        try:
            # Export members
            self.cursor.execute("SELECT * FROM members")
            members = self.cursor.fetchall()
            with open('members.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Name', 'Address', 'Contact Info'])
                writer.writerows(members)
            
            # Export parcels
            self.cursor.execute("SELECT * FROM parcels")
            parcels = self.cursor.fetchall()
            with open('parcels.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Number', 'Size', 'Location'])
                writer.writerows(parcels)
            
            # Export contributions
            self.cursor.execute("SELECT * FROM contributions")
            contributions = self.cursor.fetchall()
            with open('contributions.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Member ID', 'Amount', 'Date', 'Payment Method'])
                writer.writerows(contributions)
            
            # Export expenses
            self.cursor.execute("SELECT * FROM expenses")
            expenses = self.cursor.fetchall()
            with open('expenses.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Description', 'Amount', 'Date', 'Category'])
                writer.writerows(expenses)
            
            messagebox.showinfo("Success", "Data exported to CSV files.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CommunityApp(root)
    root.mainloop()
