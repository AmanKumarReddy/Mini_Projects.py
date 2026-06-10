import tkinter as tk
from tkinter import messagebox
import random
import ctypes
import os

class SlidingPuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Matrix: Puzzle Rearrangement")
        self.root.geometry("550x650")
        self.root.config(bg="#0d0d13")
  
        
        self.mci = ctypes.windll.winmm.mciSendStringW
        
        # 3x3 Grid settings (Numbers 1 to 8, and an empty string for the blank tile)
        self.correct_layout = [1, 2, 3, 4, 5, 6, 7, 8, ""]
        self.current_layout = []
        
        self.moves = 0
        self.game_running = False
        self.first_boot = True
        
        self.main_container = tk.Frame(self.root, bg="#0d0d13")
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
        
        title = tk.Label(self.main_container, text="NEON MATRIX PUZZLE", font=("Helvetica", 24, "bold"), fg="#ff9f43", bg="#0d0d13")
        title.pack(pady=35)
        
        desc_frame = tk.Frame(self.main_container, bg="#1a1a24", padx=20, pady=20, highlightbackground="#2c2c3e", highlightthickness=2)
        desc_frame.pack(pady=15, padx=40, fill=tk.X)
        
        desc_title = tk.Label(desc_frame, text="System Objectives:", font=("Helvetica", 13, "bold"), fg="#00d2d3", bg="#1a1a24")
        desc_title.pack(anchor="w")
        
        instructions = "1. Enter the assembly lobby and click START MISSION.\n2. A 3x3 matrix grid will generate shuffled numeric tiles.\n3. Click any tile adjacent to the blank space to slide it.\n4. Rearrange the layout sequentially from 1 to 8."
        desc_text = tk.Label(desc_frame, text=instructions, font=("Helvetica", 10), fg="#b4b4c7", bg="#1a1a24", justify="left")
        desc_text.pack(pady=10, anchor="w")
        
        next_btn = tk.Button(self.main_container, text="INITIALIZE LOBBY ➡️", font=("Helvetica", 11, "bold"), bg="#00d2d3", fg="#0d0d13",
                             activebackground="#1dd1a1", relief="flat", padx=25, pady=12, command=self.show_start_screen)
        next_btn.pack(pady=45)

    def show_start_screen(self):
        self.clean_container()
        
        if self.game_running:
            self.stop_audio("bgmusic")
            self.stop_audio("victory")
            self.play_audio("victory_sound.mp3", "victory", loop=True)
            
        self.game_running = False
        
        nav_frame = tk.Frame(self.main_container, bg="#0d0d13")
        nav_frame.pack(fill=tk.X, padx=15, pady=10)
        
        home_btn = tk.Button(nav_frame, text=" 🏠 HOME ", font=("Helvetica", 10, "bold"), bg="#ee5253", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        info_panel = tk.Frame(self.main_container, bg="#1a1a24", width=400, height=280, highlightbackground="#2c2c3e", highlightthickness=1)
        info_panel.pack(pady=40)
        info_panel.pack_propagate(False)
        
        lobby_title = tk.Label(info_panel, text="GRID CORE ONLINE", font=("Helvetica", 16, "bold"), fg="#ff9f43", bg="#1a1a24")
        lobby_title.pack(pady=35)
        
        desc_lbl = tk.Label(info_panel, text="Logic constraints compiled successfully.\nPress below to engage matrix realignment.", font=("Helvetica", 11), fg="#b4b4c7", bg="#1a1a24")
        desc_lbl.pack(pady=5)
        
        start_btn = tk.Button(info_panel, text="ENGAGE MATRIX 🚀", font=("Helvetica", 12, "bold"), bg="#ff9f43", fg="#0d0d13",
                              padx=20, pady=10, relief="flat", command=self.start_game_action)
        start_btn.pack(pady=40)

    def start_game_action(self):
        self.stop_audio("victory")
        self.play_audio("bg_music.mp3", "bgmusic", loop=True)
        
        self.moves = 0
        self.game_running = True
        
        # Shuffle loop that guarantees a solvable puzzle state
        while True:
            self.current_layout = list(self.correct_layout)
            random.shuffle(self.current_layout)
            if self.is_solvable(self.current_layout) and self.current_layout != self.correct_layout:
                break
                
        self.setup_gameplay_ui()
        self.render_grid_tiles()

    def is_solvable(self, puzzle):
        """Mathematical verification calculation determining if a shuffled 15/8 puzzle matrix is solvable."""
        inversions = 0
        arr = [x for x in puzzle if x != ""]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inversions += 1
        return inversions % 2 == 0

    def setup_gameplay_ui(self):
        self.clean_container()
        
        control_frame = tk.Frame(self.main_container, bg="#0d0d13")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        home_btn = tk.Button(control_frame, text=" 🏠 HOME ", font=("Helvetica", 9, "bold"), bg="#ee5253", fg="white", relief="flat", command=self.show_home_screen)
        home_btn.pack(side=tk.LEFT)
        
        restart_btn = tk.Button(control_frame, text=" 🔄 RESTART ", font=("Helvetica", 9, "bold"), bg="#00d2d3", fg="#0d0d13", relief="flat", command=self.show_start_screen)
        restart_btn.pack(side=tk.RIGHT)
        
        stats_frame = tk.Frame(self.main_container, bg="#0d0d13")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.moves_label = tk.Label(stats_frame, text="Matrix Shifts: 0", font=("Helvetica", 13, "bold"), fg="#ff9f43", bg="#0d0d13")
        self.moves_label.pack(side=tk.LEFT, padx=40)
        
        # Central housing matrix grid frame
        self.grid_housing = tk.Frame(self.main_container, bg="#2c2c3e", padx=10, pady=10)
        self.grid_housing.pack(pady=20)

    def render_grid_tiles(self):
        # Clear previous grid elements
        for widget in self.grid_housing.winfo_children():
            widget.destroy()
            
        for index, value in enumerate(self.current_layout):
            row = index // 3
            col = index % 3
            
            if value != "":
                btn = tk.Button(self.grid_housing, text=str(value), font=("Helvetica", 20, "bold"), width=5, height=2,
                                bg="#1a1a24", fg="#ff9f43", activebackground="#ff9f43", activeforeground="#0d0d13",
                                relief="flat", highlightbackground="#2c2c3e", command=lambda idx=index: self.tile_click_action(idx))
                btn.grid(row=row, column=col, padx=5, pady=5)
            else:
                # Render the blank space tile
                blank = tk.Label(self.grid_housing, text="", font=("Helvetica", 20, "bold"), width=5, height=2, bg="#2c2c3e")
                blank.grid(row=row, column=col, padx=5, pady=5)

    def tile_click_action(self, clicked_idx):
        if not self.game_running:
            return
            
        blank_idx = self.current_layout.index("")
        
        clicked_row, clicked_col = clicked_idx // 3, clicked_idx % 3
        blank_row, blank_col = blank_idx // 3, blank_idx % 3
        
        # Verify adjacency requirement (horizontal or vertical distance exactly equals 1)
        if (clicked_row == blank_row and abs(clicked_col - blank_col) == 1) or \
           (clicked_col == blank_col and abs(clicked_row - blank_row) == 1):
            
            import winsound
            winsound.Beep(1000, 60)
            
            # Swap data values inside the array layout
            self.current_layout[blank_idx], self.current_layout[clicked_idx] = self.current_layout[clicked_idx], self.current_layout[blank_idx]
            self.moves += 1
            self.moves_label.config(text=f"Matrix Shifts: {self.moves}")
            
            self.render_grid_tiles()
            self.verify_victory_condition()

    def verify_victory_condition(self):
        if self.current_layout == self.correct_layout:
            self.game_running = False
            import winsound
            winsound.Beep(1500, 300)
            messagebox.showinfo("Matrix Cleared", f"Victory! Puzzle array fully realigned.\nTotal shifts logged: {self.moves} 🎉")
            self.show_start_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlidingPuzzleGame(root)
    root.mainloop()