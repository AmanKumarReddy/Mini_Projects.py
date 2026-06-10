import tkinter as tk
from tkinter import messagebox
import random
import time
import winsound
import ctypes
import os

class WordScramblePremium:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Scramble Arcade")
        self.root.geometry("550x600")
        self.root.config(bg="#1e1e2e")
        
        self.mci = ctypes.windll.winmm.mciSendStringW
        
        self.word_bank = {
            1: ["cat", "dog", "sun", "map", "box", "ice", "fly", "run", "sky", "cup"],
            2: ["blue", "game", "code", "star", "fire", "wind", "tree", "ship", "gold", "fish"],
            3: ["apple", "grape", "train", "house", "smart", "clock", "water", "light", "piano", "smile"],
            4: ["python", "camera", "planet", "guitar", "window", "orange", "flight", "silver", "garden", "market"],
            5: ["network", "monitor", "browser", "weather", "journey", "counter", "diamond", "package", "vintage", "science"],
            6: ["keyboard", "database", "software", "designer", "security", "notebook", "hospital", "mountain", "tropical", "document"],
            7: ["developer", "framework", "interface", "apartment", "beautiful", "wonderful", "dangerous", "breakfast", "knowledge", "structure"],
            8: ["technology", "university", "connection", "smartphone", "collection", "management", "government", "investment", "production", "background"]
        }
        
        self.selected_level = 1
        self.original_word = ""
        self.scrambled_word = ""
        self.score = 0
        self.start_time = None
        self.game_running = False
        self.first_boot = True
        
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
        
        title = tk.Label(self.main_container, text="WORD SCRAMBLE", font=("Helvetica", 26, "bold"), fg="#f1fa8c", bg="#1e1e2e")
        title.pack(pady=20)
        
        desc_frame = tk.Frame(self.main_container, bg="#282a36", padx=15, pady=15, highlightbackground="#44475a", highlightthickness=1)
        desc_frame.pack(pady=10, padx=40, fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text="How To Play:", font=("Helvetica", 12, "bold"), fg="#50fa7b", bg="#282a36")
        desc_title.pack(anchor="w")
        
        instructions = "1. Select a level based on word length.\n2. Hit START to activate the game tracking systems.\n3. Unscramble the letters and press Enter to score!\n4. Use Restart or Home to clear and change metrics."
        desc_text = tk.Label(desc_frame, text=instructions, font=("Helvetica", 10), fg="#f8f8f2", bg="#282a36", justify="left")
        desc_text.pack(pady=5, anchor="w")
        
        lvl_title = tk.Label(self.main_container, text="Select Game Difficulty Level:", font=("Helvetica", 12, "bold"), fg="#8be9fd", bg="#1e1e2e")
        lvl_title.pack(pady=15)
        
        grid_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        grid_frame.pack(pady=5)
        
        for i in range(1, 9):
            row = (i - 1) // 2
            col = (i - 1) % 2
            btn_text = f"Level {i} ({i+2} Letters)"
            btn = tk.Button(grid_frame, text=btn_text, font=("Helvetica", 11, "bold"), width=18, bg="#6272a4", fg="#f8f8f2",
                            activebackground="#bd93f9", relief="flat", command=lambda l=i: self.select_level_action(l))
            btn.grid(row=row, column=col, padx=10, pady=8)

    def select_level_action(self, lvl):
        self.selected_level = lvl
        self.show_start_screen()

    def show_start_screen(self):
        if self.game_running:
            self.stop_audio("bgmusic")
            self.stop_audio("victory")
            self.play_audio("victory_sound.mp3", "victory", loop=True)
        
        self.game_running = False
        self.clean_container()
        
        nav_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        nav_frame.pack(fill=tk.X, padx=15, pady=10)
        
        home_btn = tk.Button(nav_frame, text=" 🏠 HOME ", font=("Helvetica", 10, "bold"), bg="#ff5555", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        info_panel = tk.Frame(self.main_container, bg="#282a36", width=380, height=300)
        info_panel.pack(pady=40)
        info_panel.pack_propagate(False)
        
        lvl_msg = f"LEVEL {self.selected_level} SELECTED"
        lvl_lbl = tk.Label(info_panel, text=lvl_msg, font=("Helvetica", 16, "bold"), fg="#ff79c6", bg="#282a36")
        lvl_lbl.pack(pady=30)
        
        len_msg = f"Target Length: {self.selected_level + 2} Letters"
        len_lbl = tk.Label(info_panel, text=len_msg, font=("Helvetica", 12), fg="#f8f8f2", bg="#282a36")
        len_lbl.pack(pady=5)
        
        start_btn = tk.Button(info_panel, text="START GAME 🚀", font=("Helvetica", 14, "bold"), bg="#50fa7b", fg="#282a36",
                              padx=20, pady=10, relief="flat", command=self.start_game_action)
        start_btn.pack(pady=40)

    def start_game_action(self):
        self.stop_audio("victory")
        self.play_audio("bg_music.mp3", "bgmusic", loop=True)
        
        self.score = 0
        self.game_running = True
        self.start_time = time.time()
        
        self.setup_gameplay_ui()
        self.generate_new_word()
        self.update_timer_loop()

    def setup_gameplay_ui(self):
        self.clean_container()
        
        control_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        home_btn = tk.Button(control_frame, text=" 🏠 HOME ", font=("Helvetica", 9, "bold"), bg="#ff5555", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        restart_btn = tk.Button(control_frame, text=" 🔄 RESTART ", font=("Helvetica", 9, "bold"), bg="#ffb86c", fg="#282a36", relief="flat", command=self.show_start_screen)
        restart_btn.pack(side=tk.RIGHT)
        
        stats_frame = tk.Frame(self.main_container, bg="#1e1e2e")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.time_label = tk.Label(stats_frame, text="Time: 0s", font=("Helvetica", 14, "bold"), fg="#ff79c6", bg="#1e1e2e")
        self.time_label.pack(side=tk.LEFT, padx=40)
        
        self.score_label = tk.Label(stats_frame, text="Score: 0", font=("Helvetica", 14, "bold"), fg="#8be9fd", bg="#1e1e2e")
        self.score_label.pack(side=tk.RIGHT, padx=40)
        
        display_panel = tk.Frame(self.main_container, bg="#282a36", highlightbackground="#44475a", highlightthickness=1)
        display_panel.pack(pady=20, padx=40, fill=tk.X)
        
        self.scrambled_label = tk.Label(display_panel, text="", font=("Helvetica", 26, "bold"), fg="#f1fa8c", bg="#282a36")
        self.scrambled_label.pack(pady=30)
        
        self.user_entry = tk.Entry(self.main_container, font=("Helvetica", 16), width=18, justify="center", bg="#f8f8f2", fg="#282a36", relief="flat")
        self.user_entry.pack(pady=15)
        self.user_entry.bind("<Return>", lambda event: self.evaluate_guess())
        self.user_entry.focus_set()
        
        submit_btn = tk.Button(self.main_container, text="SUBMIT RESPONSE ✔", font=("Helvetica", 11, "bold"), bg="#50fa7b", fg="#282a36",
                               padx=15, pady=8, relief="flat", command=self.evaluate_guess)
        submit_btn.pack(pady=10)

    def update_timer_loop(self):
        if self.game_running:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer_loop)

    def generate_new_word(self):
        self.user_entry.delete(0, tk.END)
        options = self.word_bank[self.selected_level]
        self.original_word = random.choice(options)
        
        word_letters = list(self.original_word)
        while True:
            random.shuffle(word_letters)
            self.scrambled_word = "".join(word_letters)
            if self.scrambled_word != self.original_word:
                break
                
        self.scrambled_label.config(text=self.scrambled_word.upper())

    def evaluate_guess(self):
        if not self.game_running:
            return
            
        guess = self.user_entry.get().strip().lower()
        if guess == self.original_word:
            import winsound
            winsound.Beep(1200, 150)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            messagebox.showinfo("Success", "That is correct! Excellent translation. 🎉")
            self.generate_new_word()
        else:
            import winsound
            winsound.Beep(300, 250)
            messagebox.showerror("Correction", "Incorrect match configuration. Rearrange and try again!")
            self.user_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordScramblePremium(root)
    root.mainloop()