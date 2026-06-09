import tkinter as tk
from tkinter import messagebox
import time
import winsound
import threading

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Alarm Clock")
        self.root.geometry("400x350")

        # Current Time Display
        self.current_time_label = tk.Label(self.root, text="", fg="darkblue", font=("Helvetica", 14, "bold"))
        self.current_time_label.pack(pady=10)
        self.update_current_time()

        # Title Label
        self.label = tk.Label(self.root, text="Set Alarm Time (24-Hour Format)", font=("Helvetica", 12, "bold"))
        self.label.pack(pady=10)

        # Time Input Frame
        self.time_frame = tk.Frame(self.root)
        self.time_frame.pack(pady=10)

        # Hour Entry
        self.hour_label = tk.Label(self.time_frame, text="Hour:", font=("Helvetica", 10))
        self.hour_label.pack(side=tk.LEFT, padx=5)
        self.hour_entry = tk.Entry(self.time_frame, width=3, font=("Helvetica", 18), justify="center")
        self.hour_entry.insert(0, "00")
        self.hour_entry.pack(side=tk.LEFT, padx=5)

        # Minute Entry
        self.minute_label = tk.Label(self.time_frame, text="Min:", font=("Helvetica", 10))
        self.minute_label.pack(side=tk.LEFT, padx=5)
        self.minute_entry = tk.Entry(self.time_frame, width=3, font=("Helvetica", 18), justify="center")
        self.minute_entry.insert(0, "00")
        self.minute_entry.pack(side=tk.LEFT, padx=5)

        # Second Entry
        self.second_label = tk.Label(self.time_frame, text="Sec:", font=("Helvetica", 10))
        self.second_label.pack(side=tk.LEFT, padx=5)
        self.second_entry = tk.Entry(self.time_frame, width=3, font=("Helvetica", 18), justify="center")
        self.second_entry.insert(0, "00")
        self.second_entry.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_label = tk.Label(self.root, text="Alarm not set", fg="blue", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=5)

        # Button Frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=15)

        # Set Alarm Button
        self.set_button = tk.Button(self.button_frame, text="Set Alarm", command=self.set_alarm, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"), width=12)
        self.set_button.pack(side=tk.LEFT, padx=5)

        # Cancel Button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_alarm, bg="#f44336", fg="white", font=("Helvetica", 10, "bold"), width=12)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        self.alarm_time = ""
        self.is_alarm_set = False
        self.alarm_active = False

    def update_current_time(self):
        """Update the current time display"""
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_current_time)

    def validate_input(self):
        """Validate hour, minute, and second inputs"""
        try:
            hour = int(self.hour_entry.get())
            minute = int(self.minute_entry.get())
            second = int(self.second_entry.get())

            if not (0 <= hour <= 23):
                messagebox.showerror("Invalid Hour", "Hour must be between 0-23")
                return False
            if not (0 <= minute <= 59):
                messagebox.showerror("Invalid Minute", "Minute must be between 0-59")
                return False
            if not (0 <= second <= 59):
                messagebox.showerror("Invalid Second", "Second must be between 0-59")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers only")
            return False

    def set_alarm(self):
        """Set the alarm time"""
        if not self.validate_input():
            return

        self.alarm_time = f"{self.hour_entry.get().zfill(2)}:{self.minute_entry.get().zfill(2)}:{self.second_entry.get().zfill(2)}"
        self.is_alarm_set = True
        self.alarm_active = True
        self.status_label.config(text=f"Alarm set for: {self.alarm_time}", fg="green")
        
        # Disable inputs while alarm is active
        self.hour_entry.config(state="disabled")
        self.minute_entry.config(state="disabled")
        self.second_entry.config(state="disabled")
        self.set_button.config(state="disabled")
        
        self.check_alarm()

    def cancel_alarm(self):
        """Cancel the active alarm"""
        if self.is_alarm_set:
            self.is_alarm_set = False
            self.alarm_active = False
            self.status_label.config(text="Alarm cancelled", fg="blue")
            
            # Enable inputs again
            self.hour_entry.config(state="normal")
            self.minute_entry.config(state="normal")
            self.second_entry.config(state="normal")
            self.set_button.config(state="normal")
        else:
            messagebox.showinfo("Info", "No alarm is currently set")

    def ring_alarm(self):
        """Ring the alarm with continuous beeps"""
        self.status_label.config(text="ALARM RINGING!", fg="red", bg="yellow")
        
        # Ring for 30 seconds with multiple beeps
        for _ in range(15):
            if not self.alarm_active:
                break
            winsound.Beep(1000, 1000)  # 1000 Hz for 1 second
            time.sleep(0.5)
        
        self.status_label.config(text="Alarm not set", fg="blue", bg="SystemButtonFace")
        self.alarm_active = False
        
        # Enable inputs after alarm finishes
        self.hour_entry.config(state="normal")
        self.minute_entry.config(state="normal")
        self.second_entry.config(state="normal")
        self.set_button.config(state="normal")

    def check_alarm(self):
        """Check if current time matches alarm time"""
        if self.is_alarm_set:
            current_time = time.strftime("%H:%M:%S")

            if current_time == self.alarm_time:
                self.is_alarm_set = False
                
                # Ring alarm in a separate thread to avoid freezing UI
                alarm_thread = threading.Thread(target=self.ring_alarm)
                alarm_thread.daemon = True
                alarm_thread.start()
                
                messagebox.showinfo("ALARM!", "Wake up! Your alarm time has arrived!")
                return
            
            self.root.after(1000, self.check_alarm)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()           
