# 🕹️ Python Mini Projects Arcade

Welcome to the **Python Mini Projects Arcade**! This repository is a curated collection of desktop applications and interactive arcade games built from scratch using Python. The collection transitions through different UI aesthetics—from classic arcade styling to vibrant jungle themes and sleek cyberpunk interfaces.

Each project is designed to demonstrate core software engineering principles, clean state management, custom layouts, and event-driven architectures.

---

## 🛠️ Tech Stack & Key Concepts

* **Language:** Python 3.x
* **GUI Engine:** Tkinter / TTK (Advanced Layout Management)
* **Audio Engine:** Windows Multimedia Extensions (`ctypes.windll.winmm`)
* **Core Concepts Covered:**
  * Component-driven UI architectures (Home → Lobby → Game flows)
  * File I/O & Data Persistence (CSV parsing and record synchronization)
  * Real-time rendering loops & Animation mechanics using a 2D coordinate plane
  * Dynamic grid-matrix rendering and mathematical validation logic
  * Character-by-character keyboard sequence binding

---

## 📂 Project Catalog

| # | Project Name | Visual Theme | Core Mechanism | Key Features |
|---|---|---|---|---|
| **01** | **Student Attendance Tracker** | Classic Desktop | CSV Data Logging | Dynamic multi-column date generation, file read/write synchronization, persistent table layout via `ttk.Treeview`. |
| **02** | **Word Scramble Puzzle** | Arcade Dark Purple | String Manipulation | Multi-screen audio tracking, letter shuffling algorithms, dynamic input parsing, custom viewport clearing. |
| **03** | **Typing Speed Test** | Arcade Dark Purple | Time Measurement | Character-to-minute calibration via standard 5-stroke WPM math, non-crashing array boundaries using zip alignments. |
| **04** | **Catch the Falling Objects** | Arcade Dark Purple | Gravity Animation | Continuous frame rendering, bounding box intersection calculations (collision detection), automated canvas-drop cycles. |
| **05** | **Wild Discovery: Animal ID** | Emerald Safari | Asset Management | Multi-choice button grids, localized scope memory management (preventing garbage collection bugs), 25-card dynamic decks. |
| **06** | **Neon Matrix: Sliding Puzzle** | Cyberpunk Amber | Matrix Grid Logic | Two-dimensional $3 \times 3$ grid spacing layouts, inversion calculation for mathematical solvability verification. |

---

## 🎮 Execution Instructions

### Prerequisites
These projects run entirely on Python's built-in libraries, meaning **no third-party terminal installations (`pip`) are required**. 
* Ensure you are running on a Windows environment (necessary for native `winsound` and `ctypes` multimedia engines).

### Audio Setup
To hear the built-in sound systems, make sure your project directory contains your background audio files:
* `victory_sound.mp3` (Plays on menus and lobbies)
* `bg_music.mp3` (Plays during active gameplay matches)

### Running a Project
Navigate to your repository directory using your command line interface and run your chosen file:

```bash
python sliding_puzzle.py
