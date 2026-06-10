import tkinter as tk
import time
import random
import winsound
import ctypes
import os

class MemoryGameFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.root.geometry("500x550")
        self.root.config(bg="#1e1e2e") 
        
        self.mci = ctypes.windll.winmm.mciSendStringW
        
        self.symbols = ["🍎", "🍎", "🍌", "🍌", "🍇", "🍇", "🍒", "🍒", 
                        "🍕", "🍕", "🍔", "🍔", "🧀","🧀","🍿","🍿"]
        
        self.buttons = []
        self.first_clicked_card = None  
        self.matched_pairs = 0          
        self.is_checking = False        
        self.moves_count = 0
        self.start_time = None
        self.game_running = False

        self.stats_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.stats_frame.pack(pady=15, fill=tk.X)
        
        self.time_label = tk.Label(self.stats_frame, text="Time: 0s", font=("Helvetica", 14, "bold"), fg="#ff79c6", bg="#1e1e2e")
        self.time_label.pack(side=tk.LEFT, padx=30)
        
        self.moves_label = tk.Label(self.stats_frame, text="Moves: 0", font=("Helvetica", 14, "bold"), fg="#8be9fd", bg="#1e1e2e")
        self.moves_label.pack(side=tk.RIGHT, padx=30)

        self.container = tk.Frame(self.root, bg="#1e1e2e")
        self.container.pack(pady=10)

        self.start_overlay = tk.Frame(self.container, bg="#282a36", width=380, height=380)
        self.start_overlay.grid(row=0, column=0, sticky="nsew")
        self.start_overlay.grid_propagate(False) 
        
        start_btn = tk.Button(self.start_overlay, text="START GAME 🚀", font=("Helvetica", 16, "bold"),
                              bg="#50fa7b", fg="#282a36", padx=20, pady=10, command=self.start_game)
        start_btn.place(relx=0.5, rely=0.5, anchor="center")

        self.grid_frame = tk.Frame(self.container, bg="#1e1e2e")
        self.grid_frame.grid(row=0, column=0, sticky="nsew")
        
        self.build_card_grid()
        self.start_overlay.lift()

    def build_card_grid(self):
        random.shuffle(self.symbols)
        self.buttons.clear()
        for i in range(16):
            btn = tk.Button(self.grid_frame, text="?", font=("Helvetica", 20, "bold"), 
                            width=4, height=2, bg="#6272a4", fg="#f8f8f2",
                            activebackground="#bd93f9", relief="flat",
                            command=lambda idx=i: self.flip_card(idx))
            row = i // 4
            col = i % 4
            btn.grid(row=row, column=col, padx=6, pady=6)
            self.buttons.append(btn)

    def start_game(self):
        self.start_overlay.grid_remove() 
        self.game_running = True
        self.start_time = time.time()
        
        if os.path.exists("bg_music.mp3"):
            self.mci('open "bg_music.mp3" type mpegvideo alias bgmusic', None, 0, 0)
            self.mci('play bgmusic repeat', None, 0, 0)
            
        self.update_timer_loop() 

    def update_timer_loop(self):
        if self.game_running:
            elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer_loop)

    def flip_card(self, idx):
        if self.is_checking or self.buttons[idx]["text"] != "?":
            return
            
        winsound.Beep(600, 80) 
        self.buttons[idx].config(text=self.symbols[idx], bg="#f8f8f2", fg="#282a36")
        
        if self.first_clicked_card is None:
            self.first_clicked_card = idx  
        else:
            self.is_checking = True  
            first_idx = self.first_clicked_card
            self.moves_count += 1
            self.moves_label.config(text=f"Moves: {self.moves_count}")
            
            if self.symbols[first_idx] == self.symbols[idx]:
                self.buttons[first_idx].config(bg="#50fa7b", fg="#282a36")
                self.buttons[idx].config(bg="#50fa7b", fg="#282a36")
                
                self.root.after(50, lambda: winsound.Beep(1200, 150)) 
                self.matched_pairs += 1
                self.reset_turn_state()
                
                if self.matched_pairs == 8:
                    self.game_running = False 
                    self.root.after(500, self.celebrate_victory)
            else:
                self.root.after(200, lambda: winsound.Beep(250, 300)) 
                self.root.after(600, lambda: self.hide_cards(first_idx, idx))

    def hide_cards(self, idx1, idx2):
        self.buttons[idx1].config(text="?", bg="#6272a4", fg="#f8f8f2")
        self.buttons[idx2].config(text="?", bg="#6272a4", fg="#f8f8f2")
        self.reset_turn_state()

    def reset_turn_state(self):
        self.first_clicked_card = None
        self.is_checking = False

    def celebrate_victory(self):
        final_time = self.time_label["text"]
        
        self.mci('stop bgmusic', None, 0, 0)
        self.mci('close bgmusic', None, 0, 0)
        
        if os.path.exists("victory_sound.mp3"):
            self.mci('open "victory_sound.mp3" type mpegvideo alias victory', None, 0, 0)
            self.mci('play victory', None, 0, 0)
        
        self.win_overlay = tk.Frame(self.container, bg="#282a36", width=380, height=380)
        self.win_overlay.grid(row=0, column=0, sticky="nsew")
        self.win_overlay.grid_propagate(False)
        
        title = tk.Label(self.win_overlay, text="VICTORY! 🎉🏆", font=("Helvetica", 24, "bold"), fg="#f1fa8c", bg="#282a36")
        title.pack(pady=30)
        
        score_text = f"You matched all pairs in:\n\n⏱️ {final_time}\n🏽 Total Moves: {self.moves_count}"
        score_label = tk.Label(self.win_overlay, text=score_text, font=("Helvetica", 14), fg="#f8f8f2", bg="#282a36", justify="center")
        score_label.pack(pady=20)
        
        reset_btn = tk.Button(self.win_overlay, text="Play Again 🔄", font=("Helvetica", 12, "bold"),
                              bg="#ff5555", fg="white", padx=15, pady=8, command=self.restart_entire_game)
        reset_btn.pack(pady=15)
        
        self.win_overlay.lift()

    def restart_entire_game(self):
        self.mci('stop victory', None, 0, 0)
        self.mci('close victory', None, 0, 0)
        
        self.moves_count = 0
        self.matched_pairs = 0
        self.first_clicked_card = None
        self.is_checking = False
        
        self.time_label.config(text="Time: 0s")
        self.moves_label.config(text="Moves: 0")
        
        self.win_overlay.destroy()
        self.build_card_grid()
        
        self.start_overlay.grid(row=0, column=0, sticky="nsew")
        self.start_overlay.lift()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGameFinal(root)
    root.mainloop()