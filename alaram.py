import tkinter as tk
from tkinter import messagebox
import time
import winsound

class AlaramClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Alaram Clock")
        self.root.geometry("200x300")

        self.label = tk.Label(self.root , text = "Set Alaram Time (24-Hour Format)" , font=("Helvetica", 12, "bold"))
        self.label.pack(pady = 10)

        self.time_frame = tk.Frame(self.root)
        self.time_frame.pack(pady = 10)

        self.hour_entry = tk.Entry(self.time_frame , width=3, font=("Helvetica",18),justify="center")
        self.hour_entry.insert(0,"00")
        self.hour_entry.pack(side=tk.LEFT , padx=5)

        self.minute_entry = tk.Entry(self.time_frame,width=3 , font=("Halvetica",18), justify="center")
        self.minute_entry.insert(0,"00")
        self.minute_entry.pack(side = tk.LEFT , padx=5)

        self.second_entry = tk.Entry(self.time_frame, width=3, font=("Helvetica",18), justify="center")
        self.second_entry.insert(0, "00")
        self.second_entry.pack(side = tk.LEFT , padx=5)

        self.status_label = tk.Label(self.root , text="Alaram not set", fg="blue", font=("Halvetica",10, "italic"))
        self.status_label.pack(pady=5)

        self.set_button = tk.Button(self.root , text="Set Alaram", command=self.set_alaram,  bg="#4CAF50", fg="white", font=("Halvetica", 10 , "bold"))
        self.set_button.pack(pady=10)

        self.alaram_time = ""
        self.is_alaram_set = False

    def set_alaram(self):
        self.alaram_time = f"{self.hour_entry.get().zfill(2)}:{self.minute_entry.get().zfill(2)}:{self.second_entry.get().zfill(2)}"
        self.is_alaram_set = True
        self.status_label.config(text = f"Alaram active for: {self.alaram_time}", fg="green")
        self.check_alaram()
    

    def check_alaram(self):
        if self.is_alaram_set:
            current_time = time.strftime("%H:%M:%S")

            if current_time == self.alaram_time:
                self.is_alaram_set = False
                self.status_label.config(text="Alaram Ringing", fg="red", bg="green")

                winsound.Beep(1000,15000)

                messagebox.showinfo("Alaram", "wake up! Time is up!")
                self.status_label.config(text="Alaram Not set",fg="blue")
                return
                
            self.root.after(1000, self.check_alaram)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlaramClock(root)
    root.mainloop()           
