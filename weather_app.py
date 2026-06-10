import tkinter as tk
from tkinter import messagebox
import requests

class WeatherApp:
    def __init__(self , root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x300")

        self.api_key = "657a3b058fcd5139f0dd511e3b247cc7"

        self.label = tk.Label(self.root , text="Enter City Name:", font=("Helvetica", 14))
        self.label.pack(pady=5)

        self.city_entry = tk.Entry(self.root , font=("Helvetica", 12),width=25)
        self.city_entry.pack(pady=5)

        self.search_btn = tk.Button(self.root ,text="Get Weather", command=self.get_weather, bg="#2196F3", fg="white", font=('Helvetica',10, "bold"))
        self.search_btn.pack(pady=10)

        self.city_label = tk.Label(self.root , text="", font=("Helvetica", 16, "bold"))
        self.city_label.pack(pady=5)

        self.temp_label = tk.Label(self.root , text="", font=("Helvetica" , 24, "bold"),fg="#FF9800")
        self.temp_label.pack(pady=5)

        self.desc_label = tk.Label(self.root , text="", font=("Helvetica", 12, "italic"))
        self.desc_label.pack(pady=5)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)

            data = response.json()

            if response.status_code == 200:
                city_name = data['name']
                temp = data['main']['temp']
                country = data["sys"]["country"]
                description = data['weather'][0]['description']

                self.city_label.config(text=f"{city_name},  {country}")
                self.temp_label.config(text=f"{temp}°C")
                self.desc_label.config(text=description.capitalize())
            else:
                messagebox.showerror("Error", f"City not found: {city}")
        except requests.ConnectionError:
            messagebox.showerror("Error", "Network error. Please check your connection.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()