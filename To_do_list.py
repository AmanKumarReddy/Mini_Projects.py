from logging import root
import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x450")

        self.label = tk.Label(self.root , text="Enter a Task:" , font=("Helvetica",  12))
        self.label.pack(pady = 5)

        self.task_entry = tk.Entry(self.root , font=("Helvetica",12), width=30)
        self.task_entry.pack(pady = 5)

        self.add_btn = tk.Button(self.root , text = "Add Task" , command=self.add_task , bg="#4CAF50", fg="white")
        self.add_btn.pack(pady = 5)

        self.task_listbox = tk.Listbox(self.root , font=("Helvetica", 12), width=35 , height=12, selectmode = tk.SINGLE)
        self.task_listbox.pack(pady = 10)

        self.delete_btn = tk.Button(self.root , text = "Delete Task", command=self.delete_task , bg="#f44336", fg="white")
        self.delete_btn.pack(pady = 5)

        self.clear_btn = tk.Button(self.root , text = "Clear All Tasks", command= self.clear_tasks,bg="#ff9800", fg="white")
        self.clear_btn.pack(pady =5)
    
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_listbox.insert(tk.END , task)
            self.task_entry.delete(0 , tk.END)
        else:
            messagebox.showwarning("Input Error" , "Please enter a task.")

    def delete_task(self):
        task_index = self.task_listbox.curselection()
        if task_index:
            self.task_listbox.delete(task_index)
            messagebox.showinfo(f"{task_index} indexed task deleted.")
        else:
            messagebox.showwarning("Selection Error" , "Please select a task to delete.")

        
    def clear_tasks(self):
        self.task_listbox.delete(0 , tk.END)
        messagebox.showinfo("Tasks Cleared" , "All tasks have been deleted.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()