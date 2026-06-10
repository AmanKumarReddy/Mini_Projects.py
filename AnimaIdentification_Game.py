import tkinter as tk
from tkinter import messagebox
import random
import ctypes
import os

class AnimalIDGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wild Discovery: Animal ID Arcade")
        self.root.geometry("550x650")
        self.root.config(bg="#0f2027")
        
        
        self.mci = ctypes.windll.winmm.mciSendStringW
        
        self.animal_data = [
            {"emoji": "🦁", "name": "Lion", "options": ["Tiger", "Lion", "Leopard", "Cougar"]},
            {"emoji": "🐘", "name": "Elephant", "options": ["Rhino", "Hippo", "Elephant", "Mammoth"]},
            {"emoji": "🐧", "name": "Penguin", "options": ["Puffin", "Penguin", "Seagull", "Albatross"]},
            {"emoji": "🦘", "name": "Kangaroo", "options": ["Wallaby", "Deer", "Kangaroo", "Antelope"]},
            {"emoji": "🐯", "name": "Tiger", "options": ["Cheetah", "Jaguar", "Tiger", "Panther"]},
            {"emoji": "🐻", "name": "Bear", "options": ["Bear", "Panda", "Koala", "Sloth"]},
            {"emoji": "🦊", "name": "Fox", "options": ["Wolf", "Jackal", "Fox", "Coyote"]},
            {"emoji": "🐵", "name": "Monkey", "options": ["Gorilla", "Chimpanzee", "Monkey", "Baboon"]},
            {"emoji": "🐸", "name": "Frog", "options": ["Toad", "Lizard", "Frog", "Salamander"]},
            {"emoji": "🦓", "name": "Zeebra", "options": ["Horse", "Zeebra", "Donkey", "Mule"]},
            {"emoji": "🦒", "name": "Giraffe", "options": ["Camel", "Giraffe", "Deer", "Moose"]},
            {"emoji": "🦛", "name": "Hippopotamus", "options": ["Rhino", "Hippopotamus", "Elephant", "Walrus"]},
            {"emoji": "🦏", "name": "Rhinoceros", "options": ["Rhinoceros", "Hippo", "Boar", "Tapir"]},
            {"emoji": "🐊", "name": "Crocodile", "options": ["Alligator", "Lizard", "Crocodile", "Snake"]},
            {"emoji": "🦉", "name": "Owl", "options": ["Eagle", "Hawk", "Owl", "Falcon"]},
            {"emoji": "🦇", "name": "Bat", "options": ["Bat", "Bird", "Moth", "Squirrel"]},
            {"emoji": "🦈", "name": "Shark", "options": ["Dolphin", "Shark", "Whale", "Swordfish"]},
            {"emoji": "🐙", "name": "Octopus", "options": ["Squid", "Jellyfish", "Octopus", "Starfish"]},
            {"emoji": "🦅", "name": "Eagle", "options": ["Vulture", "Falcon", "Eagle", "Raven"]},
            {"emoji": "🦆", "name": "Duck", "options": ["Goose", "Swan", "Duck", "Pigeon"]},
            {"emoji": "🐢", "name": "Turtle", "options": ["Tortoise", "Turtle", "Snail", "Crab"]},
            {"emoji": "🐍", "name": "Snake", "options": ["Python", "Viper", "Snake", "Worm"]},
            {"emoji": "🐫", "name": "Camel", "options": ["Llama", "Alpaca", "Camel", "Donkey"]},
            {"emoji": "🦩", "name": "Flamingo", "options": ["Stork", "Heron", "Flamingo", "Crane"]},
            {"emoji": "🦔", "name": "Hedgehog", "options": ["Porcupine", "Hedgehog", "Mouse", "Mole"]}
        ]
        
        self.score = 0
        self.question_index = 0
        self.max_questions = 10
        self.game_running = False
        self.first_boot = True
        
        self.main_container = tk.Frame(self.root, bg="#0f2027")
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
        
        title = tk.Label(self.main_container, text="WILD DISCOVERY", font=("Helvetica", 26, "bold"), fg="#f1c40f", bg="#0f2027")
        title.pack(pady=35)
        
        desc_frame = tk.Frame(self.main_container, bg="#203a43", padx=20, pady=20, highlightbackground="#2c5364", highlightthickness=1)
        desc_frame.pack(pady=15, padx=40, fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text="Expedition Rules:", font=("Helvetica", 14, "bold"), fg="#2ecc71", bg="#203a43")
        desc_title.pack(anchor="w")
        
        instructions = "1. Enter the staging lobby and click START.\n2. Study the large wildlife icon displayed on screen.\n3. Analyze the four multiple-choice options.\n4. Complete 10 random rounds to secure your final score."
        desc_text = tk.Label(desc_frame, text=instructions, font=("Helvetica", 11), fg="#eceff1", bg="#203a43", justify="left")
        desc_text.pack(pady=10, anchor="w")
        
        next_btn = tk.Button(self.main_container, text="START EXPEDITION ➡️", font=("Helvetica", 12, "bold"), bg="#2ecc71", fg="white",
                             activebackground="#27ae60", relief="flat", padx=25, pady=12, command=self.show_start_screen)
        next_btn.pack(pady=45)

    def show_start_screen(self):
        self.clean_container()
        
        if self.game_running:
            self.stop_audio("bgmusic")
            self.stop_audio("victory")
            self.play_audio("victory_sound.mp3", "victory", loop=True)
            
        self.game_running = False
        
        nav_frame = tk.Frame(self.main_container, bg="#0f2027")
        nav_frame.pack(fill=tk.X, padx=15, pady=10)
        
        home_btn = tk.Button(nav_frame, text=" 🏠 HOME ", font=("Helvetica", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        info_panel = tk.Frame(self.main_container, bg="#203a43", width=400, height=280)
        info_panel.pack(pady=40)
        info_panel.pack_propagate(False)
        
        lobby_title = tk.Label(info_panel, text="LOBBY CONNECTION SET", font=("Helvetica", 16, "bold"), fg="#f1c40f", bg="#203a43")
        lobby_title.pack(pady=35)
        
        desc_lbl = tk.Label(info_panel, text="Vector glyph modules are initialized.\nPress below to engage testing modules.", font=("Helvetica", 11), fg="#eceff1", bg="#203a43")
        desc_lbl.pack(pady=5)
        
        start_btn = tk.Button(info_panel, text="ENGAGE SYSTEM 🚀", font=("Helvetica", 13, "bold"), bg="#2ecc71", fg="white",
                              padx=20, pady=10, relief="flat", command=self.start_game_action)
        start_btn.pack(pady=40)

    def start_game_action(self):
        self.stop_audio("victory")
        self.play_audio("bg_music.mp3", "bgmusic", loop=True)
        
        self.score = 0
        self.question_index = 0
        self.game_running = True
        random.shuffle(self.animal_data)
        
        self.setup_gameplay_ui()
        self.load_next_question()

    def setup_gameplay_ui(self):
        self.clean_container()
        
        control_frame = tk.Frame(self.main_container, bg="#0f2027")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        home_btn = tk.Button(control_frame, text=" 🏠 HOME ", font=("Helvetica", 9, "bold"), bg="#e74c3c", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        restart_btn = tk.Button(control_frame, text=" 🔄 RESTART ", font=("Helvetica", 9, "bold"), bg="#f39c12", fg="white", relief="flat", command=self.show_start_screen)
        restart_btn.pack(side=tk.RIGHT)
        
        stats_frame = tk.Frame(self.main_container, bg="#0f2027")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(stats_frame, text=f"Score: 0/{self.max_questions}", font=("Helvetica", 13, "bold"), fg="#2ecc71", bg="#0f2027")
        self.score_label.pack(side=tk.LEFT, padx=40)
        
        self.image_container = tk.Label(self.main_container, text="", font=("Helvetica", 82), bg="#203a43", width=6, height=2,
                                        highlightbackground="#2c5364", highlightthickness=2)
        self.image_container.pack(pady=15)
        
        self.button_frame = tk.Frame(self.main_container, bg="#0f2027")
        self.button_frame.pack(pady=15)
        
        self.option_buttons = []
        for i in range(4):
            row = i // 2
            col = i % 2
            btn = tk.Button(self.button_frame, text="", font=("Helvetica", 11, "bold"), width=16, height=2, bg="#2c3e50", fg="#eceff1",
                            activebackground="#34495e", activeforeground="white", relief="flat", command=lambda idx=i: self.evaluate_choice(idx))
            btn.grid(row=row, column=col, padx=12, pady=12)
            self.option_buttons.append(btn)

    def load_next_question(self):
        if self.question_index < self.max_questions and self.question_index < len(self.animal_data):
            current_item = self.animal_data[self.question_index]
            
            self.image_container.config(text=current_item["emoji"])
                
            for i, option in enumerate(current_item["options"]):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            self.game_running = False
            messagebox.showinfo("Quiz Over", f"Expedition complete!\nYour Final Score: {self.score} / {self.max_questions} 🎉")
            self.show_start_screen()

    def evaluate_choice(self, chosen_idx):
        if not self.game_running:
            return
            
        current_item = self.animal_data[self.question_index]
        selected_answer = self.option_buttons[chosen_idx].cget("text")
        
        import winsound
        if selected_answer == current_item["name"]:
            winsound.Beep(1200, 150)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}/{self.max_questions}")
            messagebox.showinfo("Correct Match", "Excellent classification! That is the right animal. 🌿")
        else:
            winsound.Beep(350, 250)
            messagebox.showerror("Incorrect Match", f"Mismatch detected! That animal is actually a {current_item['name']}.")
            
        self.question_index += 1
        self.load_next_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalIDGame(root)
    root.mainloop()