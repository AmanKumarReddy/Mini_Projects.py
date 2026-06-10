import tkinter as tk
from tkinter import messagebox

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x300")

        self.expenses = []

        self.desc_label = tk.Label(self.root , text="Expense Description:" , font=("Helvetica" , 11))
        self.desc_label.pack(pady=2)
        self.desc_entry = tk.Entry(self.root , width=30)
        self.desc_entry.pack(pady=2)

        self.amount_label = tk.Label(self.root , text="Expense Amount:", font=("Helvetica" , 11))
        self.amount_label.pack(pady=2)
        self.amt_entry = tk.Entry(self.root , font=("Helvetica", 11),width=30)
        self.amt_entry.pack(pady=5)

        self.add_btn = tk.Button(self.root , text = "Add Expense", command=self.add_expense , bg="#4CAF50" , fg="white", font=("Helvetica", 10, "bold"))
        self.add_btn.pack(pady=5)

        self.list_label = tk.Label(self.root , text="History:", font=("Helvetica", 11, "bold"))
        self.list_label.pack(pady=5)

        self.expense_listbox = tk.Listbox(self.root , font=("Helvetica", 11), width=35, height=12)
        self.expense_listbox.pack(pady=5)

        self.total_label = tk.Label(self.root , text="Total Spending: $0.00", fg="red", font=("Helvetica", 14, "bold"))
        self.total_label.pack(pady=10)

        self.delete_btn = tk.Button(self.root , text="Delete Selected", command=self.delete_expense, bg="#f44336", fg="white")
        self.delete_btn.pack(pady=5)
    
    def add_expense(self):
        desc = self.desc_entry.get().strip()
        amt = self.amt_entry.get().strip()
        if not desc or not amt:
            messagebox.showwarning("Input Error", "Please fill our both fileds")
            return
        try:
            amt = float(amt)
            if amt<0:
                messagebox.showerror("Input Error" , "Amount must be greater than zero")
                return
            self.expenses.append(amt)
            display_text = f"{desc} - ${amt:.2f}"
            self.expense_listbox.insert(tk.END , display_text)
            self.update_total()

            self.desc_entry.delete(0, tk.END)
            self.amt_entry.delete(0, tk.END)
        except ValueError:
             messagebox.showerror("Error" , "Please enter a valid number fot the amount")

    def delete_expense(self):
        try:
            selected_index = self.expense_listbox.curselection()[0]
            self.expenses.pop(selected_index)
            self.expense_listbox.delete(selected_index)
            self.update_total()
        except IndexError:
             messagebox.showerror("Error", "Please select an item to delete")

    def update_total(self):
         total = sum(self.expenses)

         self.total_label.config(text=f"Total Spending: ${total:.2f}")
         

    
if __name__ == "__main__":
            root = tk.Tk()
            app = ExpenseTracker(root)
            root.mainloop()