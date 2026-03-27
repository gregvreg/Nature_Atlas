import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
IMAGE_DIR = os.path.join(PROJECT_DIR, "data", "images")
DB_NAME = os.path.join(BASE_DIR, "atlas_animaux.db")


def launch_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    subprocess.Popen([sys.executable, script_path], cwd=BASE_DIR)


def ensure_database():
    needs_init = not os.path.exists(DB_NAME) or os.path.getsize(DB_NAME) == 0
    if not needs_init:
        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Especes'")
            needs_init = cur.fetchone() is None
            conn.close()
        except sqlite3.Error:
            needs_init = True
    if not needs_init:
        return

    from atlas_animaux import create_database

    create_database()


def play_quiz():
    launch_script("Quiz.py")
    sys.exit()

def play_carte():
    launch_script("carte.py")
    sys.exit()

# ── FENÊTRE PRINCIPALE ──
ensure_database()

root = tk.Tk()
root.title("Nature Atlas")
root.configure(bg="#09471c")

root.state('zoomed')
root.update_idletasks()
SCR_W = root.winfo_screenwidth()
SCR_H = root.winfo_screenheight()

# Polices
TF  = tkfont.Font(family="Courier New", size=28, weight="bold")
SF  = tkfont.Font(family="Courier New", size=12, slant="italic")
BF  = tkfont.Font(family="Courier New", size=12, weight="bold")
MF  = tkfont.Font(family="Courier New", size=14, weight="bold")
LF  = tkfont.Font(family="Courier New", size=10, weight="bold")
DF  = tkfont.Font(family="Courier New", size=11)

HEADER_H = 90

# ── EN-TÊTE ──
hdr = tk.Frame(root, bg="#09471c", height=HEADER_H)
hdr.pack(fill="x", side="top")
hdr.pack_propagate(False)

tk.Label(hdr, text="Nature Atlas",
         font=TF, fg="white", bg="#09471c").pack(pady=(14, 2))
tk.Label(hdr, text="Découvrez la richesse de notre planète",
         font=SF, fg="#a8d8a8", bg="#09471c").pack()
tk.Frame(hdr, bg="lightgreen", height=2).pack(fill="x", padx=60, pady=(6, 0))

# ── CORPS ──
body = tk.Frame(root, bg="#0a1a0a")
body.pack(fill="both", expand=True)

# ── PANNEAU GAUCHE ──
LEFT_W = 380
left = tk.Frame(body, bg="#0a1a0a", width=LEFT_W)
left.pack(side="left", fill="y")
left.pack_propagate(False)

tk.Frame(left, bg="#0a1a0a").pack(expand=True)

tk.Label(left, text="NAVIGATION",
         font=tkfont.Font(family="Courier New", size=10, weight="bold"),
         fg="#34c759", bg="#0a1a0a").pack(pady=(0, 6), padx=30, anchor="w")
tk.Frame(left, bg="#34c759", height=1).pack(fill="x", padx=30, pady=(0, 30))

# ── Bouton CARTE ──
def on_enter_carte(e):
    btn_carte.configure(bg="#34c759", fg="#0a1a0a")
    desc_carte.configure(fg="#34c759")

def on_leave_carte(e):
    btn_carte.configure(bg="#0f2a0f", fg="#34c759")
    desc_carte.configure(fg="#7aaa7a")

carte_frame = tk.Frame(left, bg="#0f2a0f", cursor="hand2")
carte_frame.pack(fill="x", padx=30, pady=10, ipady=10)

btn_carte = tk.Label(carte_frame, text="◉  Accès à la carte",
                     font=MF, fg="#34c759", bg="#0f2a0f",
                     anchor="w", padx=20, cursor="hand2")
btn_carte.pack(fill="x")

desc_carte = tk.Label(carte_frame,
                      text="Explorez les animaux du monde entier\nsur une carte interactive.",
                      font=DF, fg="#7aaa7a", bg="#0f2a0f",
                      anchor="w", padx=20, justify="left")
desc_carte.pack(fill="x")

for w in (carte_frame, btn_carte, desc_carte):
    w.bind("<Button-1>", lambda e: play_carte())
    w.bind("<Enter>", on_enter_carte)
    w.bind("<Leave>", on_leave_carte)

# ── Bouton QUIZ ──
def on_enter_quiz(e):
    btn_quiz.configure(bg="#1e88e5", fg="#0a1a0a")
    desc_quiz.configure(fg="#1e88e5")

def on_leave_quiz(e):
    btn_quiz.configure(bg="#0f1f3a", fg="#1e88e5")
    desc_quiz.configure(fg="#5a9ad9")

quiz_frame = tk.Frame(left, bg="#0f1f3a", cursor="hand2")
quiz_frame.pack(fill="x", padx=30, pady=10, ipady=10)

btn_quiz = tk.Label(quiz_frame, text="◉  Faire le quiz",
                    font=MF, fg="#1e88e5", bg="#0f1f3a",
                    anchor="w", padx=20, cursor="hand2")
btn_quiz.pack(fill="x")

desc_quiz = tk.Label(quiz_frame,
                     text="Testez vos connaissances sur les\nanimaux et leurs régions d'origine.",
                     font=DF, fg="#5a9ad9", bg="#0f1f3a",
                     anchor="w", padx=20, justify="left")
desc_quiz.pack(fill="x")

for w in (quiz_frame, btn_quiz, desc_quiz):
    w.bind("<Button-1>", lambda e: play_quiz())
    w.bind("<Enter>", on_enter_quiz)
    w.bind("<Leave>", on_leave_quiz)

tk.Frame(left, bg="#0a1a0a").pack(expand=True)

tk.Frame(body, bg="#34c759", width=2).pack(side="left", fill="y", pady=20)

# ── PANNEAU DROIT ──
right = tk.Frame(body, bg="#0a1a0a")
right.pack(side="left", fill="both", expand=True)

# Grille d'images
grid = tk.Frame(right, bg="#0a1a0a")
grid.pack(fill="both", expand=True, padx=20, pady=20)

grid.columnconfigure(0, weight=1)
grid.columnconfigure(1, weight=1)
grid.rowconfigure(0, weight=1)
grid.rowconfigure(1, weight=1)

IMG_SOURCES = [
    ("monde.png",    "🌍  Carte du monde",      "#34c759", "#0f2a0f"),
    ("Quiz.png",      "🧠  Quiz nature",         "#1e88e5", "#0f1f3a"),
]

# Couleurs de secours pour les cadres sans image
FALLBACK_DATA = [
    ("#0f2a0f", "#34c759", "🌍\n\nCarte Interactive\n\nExplorez les régions\ndu monde entier"),
    ("#0f1f3a", "#1e88e5", "🧠\n\nQuiz Nature\n\n100 animaux à deviner\nScore sur 10"),
    ("#1a1a0a", "#d9c44a", "🦁\n\n100 Animaux\n\nDes 5 continents\net des pôles"),
    ("#1a0a1a", "#d94a8a", "🗺️\n\n10 Régions\n\nAfrique, Europe, Asie,\nAmériques et plus"),
]

IMAGE_FILES = [
    os.path.join(IMAGE_DIR, "monde.png"),
    os.path.join(IMAGE_DIR, "Quiz.png"),
]

img_refs = []

positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

for idx, (row, col) in enumerate(positions):
    bg_c, fg_c, fallback_text = FALLBACK_DATA[idx]

    cell = tk.Frame(grid, bg=bg_c)
    cell.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    # Chargement de l'image
    loaded = False
    if idx < len(IMAGE_FILES):
        fp = IMAGE_FILES[idx]
        if os.path.exists(fp):
            try:
                img = Image.open(fp).convert("RGB")
                img_photo_raw = img
                loaded = True
            except Exception:
                pass

    if loaded:
        root.update_idletasks()
        cw = max(1, (SCR_W - LEFT_W - 80) // 2 - 16)
        ch = max(1, (SCR_H - HEADER_H - 40) // 2 - 16)
        img_resized = img_photo_raw.resize((cw, ch), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)
        img_refs.append(photo)
        lbl = tk.Label(cell, image=photo, bg=bg_c)
        lbl.pack(fill="both", expand=True)
    else:
        tk.Label(cell, text=fallback_text,
                 font=tkfont.Font(family="Courier New", size=13, weight="bold"),
                 fg=fg_c, bg=bg_c, justify="center").pack(expand=True)

    tag = tk.Label(cell, text=f"  {FALLBACK_DATA[idx][2].split(chr(10))[2].strip() if chr(10) in FALLBACK_DATA[idx][2] else ''}  ",
                   font=LF, fg="#0a1a0a", bg=fg_c)
    tag.place(relx=0.0, rely=1.0, anchor="sw")

root._img_refs = img_refs

root.mainloop()
