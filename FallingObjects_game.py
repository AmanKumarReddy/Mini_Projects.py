import tkinter as tk
from tkinter import messagebox
import random
import ctypes
import os

class CatchObjectsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Falling Objects")
        self.root.geometry("600x650")
        self.root.config(bg="#1e1e2e")
        
        
        self.mci = ctypes.windll.winmm.mciSendStringW
        
        self.score = 0
        self.missed = 0
        self.game_running = False
        self.first_boot = True
        
        self.falling_speed = 7
        self.spawn_rate = 1500
        
        self.basket_x = 250
        self.basket_width = 100
        self.basket_speed = 35
        
        self.objects = []
        
        self.main_container = tk.Frame(self.root, bg="#1e1e2e")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.show_home_screen()

    def play_audio(self, filename, alias, loop=False):
        if os.path.exists(filename):
            self.mci(f'open "{filename}" type mpegvideo alias {alias}', None, 0, 0)
            command = f'play {alias} repeat' if loop else f'play {alias}'
            self.mci(command, None, 0, 0)

    def stop_audio(self, alias):
        self.mci(f'stop {alias}', None, 0, 0)
        self.mci(f'close {alias}', None, 0, 0)

    def clean_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        if self.game_running or self.first_boot:
            self.stop_audio("bgmusic")
            self.stop_audio("victory")
            self.play_audio("victory_sound.mp3", "victory", loop=True)
            self.first_boot = False
            
        self.game_running = False
        self.clean_container()
        
        title = tk.Label(self.main_container, text="CATCH THE OBJECTS", font=("Helvetica", 26, "bold"), fg="#f1fa8c", bg="#1e1e2e")
        title.pack(pady=30)
        
        desc_frame = tk.Frame(self.main_container, bg="#282a36", padx=20, pady=20, highlightbackground="#44475a", highlightthickness=1)
        desc_frame.pack(pady=20, padx=50, fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text="Arcade Instructions:", font=("Helvetica", 14, "bold"), fg="#50fa7b", bg="#282a36")
        desc_title.pack(anchor="w")
        
        instructions = "1. Use Left and Right arrow keys to move your basket.\n2. Catch falling items to score points.\n3. If you miss 5 items, the game tracking loop terminates.\n4. Press Home or Restart at any point to reset."
        desc_text = tk.Label(desc_frame, text=instructions, font=("Helvetica", 11), fg="#f8f8f2", bg="#282a36", justify="left")
        desc_text.pack(pady=10, anchor="w")
        
        next_btn = tk.Button(self.main_container, text="GO TO LOBBY ➡️", font=("Helvetica", 14, "bold"), bg="#6272a4", fg="#f8f8f2",
                             activebackground="#bd93f9", relief="flat", padx=25, pady=10, command=self.show_start_screen)
        next_btn.pack(pady=40)

    def show_start_screen(self):
        self.clean_container()
        
        if self.game_running:
            self.stop_audio("bgmusic")
            self.stop_audio("victory")
            self.play_audio("victory_sound.mp3", "victory", loop=True)
            
        self.game_running = False
        self.objects.clear()
        
        nav_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        nav_frame.pack(fill=tk.X, padx=15, pady=10)
        
        home_btn = tk.Button(nav_frame, text=" 🏠 HOME ", font=("Helvetica", 10, "bold"), bg="#ff5555", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        info_panel = tk.Frame(self.main_container, bg="#282a36", width=420, height=280)
        info_panel.pack(pady=40)
        info_panel.pack_propagate(False)
        
        lobby_title = tk.Label(info_panel, text="READY PLAYER ONE", font=("Helvetica", 16, "bold"), fg="#ff79c6", bg="#282a36")
        lobby_title.pack(pady=35)
        
        desc_lbl = tk.Label(info_panel, text="Catch items drop downward.\nSpeed escalates as points grow.", font=("Helvetica", 12), fg="#f8f8f2", bg="#282a36")
        desc_lbl.pack(pady=5)
        
        start_btn = tk.Button(info_panel, text="START MISSION 🚀", font=("Helvetica", 14, "bold"), bg="#50fa7b", fg="#282a36",
                              padx=20, pady=10, relief="flat", command=self.start_game_action)
        start_btn.pack(pady=35)

    def start_game_action(self):
        self.stop_audio("victory")
        self.play_audio("bg_music.mp3", "bgmusic", loop=True)
        
        self.score = 0
        self.missed = 0
        self.falling_speed = 7
        self.game_running = True
        
        self.setup_gameplay_ui()
        self.spawn_object_loop()
        self.update_animation_loop()

    def setup_gameplay_ui(self):
        self.clean_container()
        
        control_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        home_btn = tk.Button(control_frame, text=" 🏠 HOME ", font=("Helvetica", 9, "bold"), bg="#ff5555", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        restart_btn = tk.Button(control_frame, text=" 🔄 RESTART ", font=("Helvetica", 9, "bold"), bg="#ffb86c", fg="#282a36", relief="flat", command=self.show_start_screen)
        restart_btn.pack(side=tk.RIGHT)
        
        stats_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(stats_frame, text="Score: 0", font=("Helvetica", 12, "bold"), fg="#50fa7b", bg="#1e1e2e")
        self.score_label.pack(side=tk.LEFT, padx=30)
        
        self.missed_label = tk.Label(stats_frame, text="Missed: 0/5", font=("Helvetica", 12, "bold"), fg="#ff5555", bg="#1e1e2e")
        self.missed_label.pack(side=tk.RIGHT, padx=30)
        
        self.canvas = tk.Canvas(self.main_container, width=600, height=450, bg="#282a36", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.basket = self.canvas.create_rectangle(self.basket_x, 420, self.basket_x + self.basket_width, 440, fill="#8be9fd", outline="")
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def move_left(self, event):
        if self.game_running and self.basket_x > 0:
            self.basket_x -= self.basket_speed
            if self.basket_x < 0:
                self.basket_x = 0
            self.canvas.coords(self.basket, self.basket_x, 420, self.basket_x + self.basket_width, 440)

    def move_right(self, event):
        if self.game_running and self.basket_x < (600 - self.basket_width):
            self.basket_x += self.basket_speed
            if self.basket_x > (600 - self.basket_width):
                self.basket_x = 600 - self.basket_width
            self.canvas.coords(self.basket, self.basket_x, 420, self.basket_x + self.basket_width, 440)

    def spawn_object_loop(self):
        if self.game_running:
            x_pos = random.randint(20, 580)
            colors = ["#ff79c6", "#bd93f9", "#f1fa8c", "#ffb86c"]
            obj = self.canvas.create_oval(x_pos, 0, x_pos + 20, 20, fill=random.choice(colors), outline="")
            self.objects.append(obj)
            self.root.after(self.spawn_rate, self.spawn_object_loop)

    def update_animation_loop(self):
        if not self.game_running:
            return
            
        objects_to_remove = []
        
        for obj in self.objects:
            self.canvas.move(obj, 0, self.falling_speed)
            coords = self.canvas.coords(obj)
            
            if coords:
                x1, y1, x2, y2 = coords
                
                if y2 >= 420 and y1 <= 440:
                    if x2 >= self.basket_x and x1 <= (self.basket_x + self.basket_width):
                        import winsound
                        winsound.Beep(1500, 100)
                        self.score += 1
                        self.score_label.config(text=f"Score: {self.score}")
                        
                        if self.score % 5 == 0:
                            self.falling_speed += 1
                            
                        self.canvas.delete(obj)
                        objects_to_remove.append(obj)
                        continue
                
                if y2 >= 450:
                    import winsound
                    winsound.Beep(400, 150)
                    self.missed += 1
                    self.missed_label.config(text=f"Missed: {self.missed}/5")
                    self.canvas.delete(obj)
                    objects_to_remove.append(obj)
                    
                    if self.missed >= 5:
                        self.game_running = False
                        messagebox.showinfo("Game Over", f"Defeat! You missed too many objects.\nFinal Score: {self.score}")
                        self.show_start_screen()
                        return

        for obj in objects_to_remove:
            if obj in self.objects:
                self.objects.remove(obj)
                
        self.root.after(30, self.update_animation_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatchObjectsGame(root)
    root.mainloop()