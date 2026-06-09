import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv

class AttendanceSystem:
    def __init__(self , root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("800x600")

        self.data_file = "attendace.csv"

        self.label = tk.Label(root , text = "Student Name: " ,font=("Halvetica" ,11))
        self.label.pack(pady=5)

        self.name_entry = tk.Entry(root , font=("Halvetica" , 11),width=30)
        self.name_entry.pack(pady=5)

        self.add_btn = tk.Button(self.root , text="Add Student", command=self.add_student, bg="#4CAF50", fg="white")
        self.add_btn.pack(pady=5)

        #New Topic that i have to learn Tables
        self.tree = ttk.Treeview(root, columns=("Name", "Status"), show="headings", height=10)
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Status", text="Attendance Status")
        self.tree.column("Name" , width=200, anchor="center")
        self.tree.column("Status" , width=150, anchor="center")
        self.tree.pack(pady=15)

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=5)

        self.present_btn = tk.Button(self.btn_frame , text="Mark Present" , command=lambda: self.mark_status("Present"), bg="#2196F3" , fg="white")
        self.present_btn.pack(side=tk.LEFT, padx=10)

        self.absent_btn = tk.Button(self.btn_frame, text="Mark Absent" , command=lambda: self.mark_status("Absent"), bg="#f44336", fg="white")
        self.absent_btn.pack(side=tk.LEFT , padx=10)

        self.load_from_csv()

    def add_student(self):
        name = self.name_entry.get().strip()
        if name:
            for row in self.tree.get_children():
                if self.tree.item(row)["values"][0] == name:
                    messagebox.showerror('Error', 'Student already exists!')
                    return
            self.tree.insert("", tk.END, values=(name , "Not Marked"))
            self.name_entry.delete(0, tk.END)
            self.save_to_csv()
        else:
            messagebox.showwarning('Input Error' , 'Please enter a student name.')

    def mark_status(self, status):
        selected_item = self.tree.selection()
        if selected_item:
            student_name = self.tree.item(selected_item)["values"][0]
            self.tree.item(selected_item, values=(student_name, status))
            self.save_to_csv()
        else:
            messagebox.showwarning('Selection Error' , 'Please select a student to mark attendace.')

    def save_to_csv(self):
        with open(self.data_file , mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in self.tree.get_children():
                row_data = self.tree.item(row)["values"]
                writer.writerow(row_data)
    
    def load_from_csv(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.tree.insert("", tk.END, values=(row[0], row[1]))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()