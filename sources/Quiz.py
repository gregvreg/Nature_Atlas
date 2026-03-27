import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw
import sqlite3
import os
import subprocess
import sys
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
ANIMAL_IMAGE_DIR = os.path.join(DATA_DIR, "animaux")
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


def resolve_animal_image_base(path):
    if not path:
        return path
    if os.path.isabs(path):
        return os.path.splitext(path)[0]
    image_name = os.path.basename(os.path.normpath(path))
    return os.path.join(ANIMAL_IMAGE_DIR, image_name)

REGION_COLORS = {
    "Afrique":                     "#e8a020",
    "Europe":                      "#4a90d9",
    "Asie":                        "#d94a4a",
    "Amérique du Nord":            "#00C735",
    "Amérique du Sud":             "#a04ad9",
    "Océanie":                     "#d97c4a",
    "Antarctique":                 "#7cbcd9",
    "Moyen-Orient":                "#d9c44a",
    "Asie du Sud-Est":             "#d94a8a",
    "Caraïbes & Amérique Centrale":"#4ad9b8",
}

REGIONS = list(REGION_COLORS.keys())
QUIZ_SIZE = 10  

# ── BASE DE DONNÉES ──
def get_all_animaux():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT e.*, r.nom_region
        FROM Especes e
        JOIN Regions r ON e.region_id = r.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def load_image(path, size):
    base_path = resolve_animal_image_base(path)
    for ext in (".jpg", ".jpeg", ".png", ".avif", ".webp", ".gif"):
        fp = base_path + ext
        if os.path.exists(fp):
            try:
                img = Image.open(fp).convert("RGB").resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception:
                pass
    img = Image.new("RGB", size, "#1a2a1a")
    ImageDraw.Draw(img).rectangle([2, 2, size[0]-3, size[1]-3],
                                   outline="#34c759", width=2)
    return ImageTk.PhotoImage(img)

def retour_menu():
    launch_script("Index.py")
    sys.exit()

# ── FENETRE PRINCIPALE ──

ensure_database()

root = tk.Tk()
root.title("Exploration Nature — Quiz")
root.configure(bg="#09471c")
root.state('zoomed')
root.update_idletasks()
SCR_W = root.winfo_screenwidth()
SCR_H = root.winfo_screenheight()

HEADER_H = 82

# Polices
TF  = tkfont.Font(family="Courier New", size=22, weight="bold")
SF  = tkfont.Font(family="Courier New", size=11, slant="italic")
BF  = tkfont.Font(family="Courier New", size=10, weight="bold")
MF  = tkfont.Font(family="Courier New", size=14, weight="bold")
LF  = tkfont.Font(family="Courier New", size=11, weight="bold")
DF  = tkfont.Font(family="Courier New", size=11)
NF  = tkfont.Font(family="Courier New", size=18, weight="bold")
QF  = tkfont.Font(family="Courier New", size=13, weight="bold")
RF  = tkfont.Font(family="Courier New", size=13)

# ── EN-TÊTE ──
hdr = tk.Frame(root, bg="#09471c", height=HEADER_H)
hdr.pack(fill="x", side="top")
hdr.pack_propagate(False)

tk.Label(hdr, text="Exploration Nature — Quiz",
         font=TF, fg="white", bg="#09471c").pack(pady=(12, 2))
tk.Label(hdr, text="De quelle région provient cet animal ?",
         font=SF, fg="#a8d8a8", bg="#09471c").pack()
tk.Frame(hdr, bg="lightgreen", height=2).pack(fill="x", padx=60, pady=(5, 0))

# ── BOUTON RETOUR ──
btn_frame = tk.Frame(root, bg="black", width=220, height=34)
btn_frame.place(x=4, y=4)
tk.Button(btn_frame, text="<<< Retourner au menu",
          bg="#34c759", fg="white", font=BF,
          relief="flat", cursor="hand2",
          command=retour_menu).pack(expand=True, fill="both")

# ── ZONE PRINCIPALE ──
main_frame = tk.Frame(root, bg="#0a1a0a")
main_frame.pack(fill="both", expand=True)

# ── ETAT DU QUIZ ──

quiz_state = {
    "animaux": [],
    "current_index": 0,
    "score": 0,
    "answered": False,
    "selected_btn": None,
}

# ── ECRAN D'ACCEUIL ──

def show_home():
    for w in main_frame.winfo_children():
        w.destroy()

    home = tk.Frame(main_frame, bg="#0a1a0a")
    home.pack(expand=True)

    tk.Label(home, text="🌿  Bienvenue dans le Quiz Nature",
             font=NF, fg="#34c759", bg="#0a1a0a").pack(pady=(40, 10))

    tk.Frame(home, bg="#34c759", height=1).pack(fill="x", padx=80, pady=(0, 30))

    regles_txt = (
        "◆  10 questions tirées aléatoirement parmi 100 animaux.\n\n"
        "◆  Pour chaque animal, devinez sa région d'origine parmi 10 choix.\n\n"
        "◆  Une seule tentative par question — le score est sur 10.\n\n"
        "◆  Consultez la carte interactive pour réviser avant de jouer !\n\n"
        "◆  Le quiz peut être rejoué autant de fois que voulu."
    )
    tk.Label(home, text=regles_txt,
             font=DF, fg="#d4e8d4", bg="#0a1a0a",
             justify="left").pack(padx=60, pady=10)

    tk.Frame(home, bg="#1a3a1a", height=1).pack(fill="x", padx=80, pady=(20, 30))

    def launch():
        start_quiz()

    launch_btn = tk.Button(home, text="▶   Lancer le quiz",
                           bg="#34c759", fg="#0a1a0a", font=MF,
                           relief="flat", cursor="hand2", padx=40, pady=14,
                           command=launch)
    launch_btn.pack()

    def on_e(e): launch_btn.configure(bg="#57e87d")
    def on_l(e): launch_btn.configure(bg="#34c759")
    launch_btn.bind("<Enter>", on_e)
    launch_btn.bind("<Leave>", on_l)

# ── DEMARRER LE QUIZ ──

def start_quiz():
    all_animaux = get_all_animaux()
    selected = random.sample(list(all_animaux), QUIZ_SIZE)
    quiz_state["animaux"] = selected
    quiz_state["current_index"] = 0
    quiz_state["score"] = 0
    quiz_state["answered"] = False
    quiz_state["selected_btn"] = None
    show_question()

# ── AFFICHER QUESTIONS ──

def show_question():
    for w in main_frame.winfo_children():
        w.destroy()

    idx = quiz_state["current_index"]
    animal = quiz_state["animaux"][idx]
    correct_region = animal["nom_region"]

    wrong_regions = random.sample([r for r in REGIONS if r != correct_region], 3)
    options = wrong_regions + [correct_region]
    random.shuffle(options)

    quiz_state["answered"] = False
    quiz_state["correct_region"] = correct_region

    content = tk.Frame(main_frame, bg="#0a1a0a")
    content.pack(fill="both", expand=True, padx=40, pady=20)

    # Colonne gauche 
    col_left = tk.Frame(content, bg="#0a1a0a")
    col_left.pack(side="left", fill="both", expand=True)

    # Colonne droite 
    col_right = tk.Frame(content, bg="#0a1a0a", width=460)
    col_right.pack(side="right", fill="y", padx=(30, 0))
    col_right.pack_propagate(False)

    # ── Barre de progression ──
    
    prog_frame = tk.Frame(col_left, bg="#0a1a0a")
    prog_frame.pack(fill="x", pady=(0, 12))

    tk.Label(prog_frame,
             text=f"Question {idx + 1} / {QUIZ_SIZE}    ●  Score : {quiz_state['score']} / {idx}",
             font=LF, fg="#7aaa7a", bg="#0a1a0a").pack(side="left")

    bar_bg = tk.Frame(prog_frame, bg="#1a3a1a", height=8, width=300)
    bar_bg.pack(side="right", pady=4)
    fill_w = int(300 * idx / QUIZ_SIZE)
    tk.Frame(bar_bg, bg="#34c759", height=8, width=fill_w).place(x=0, y=0)

    img_frame = tk.Frame(col_left, bg="#1a3a1a")
    img_frame.pack(pady=(0, 16))

    root.update_idletasks()
    img_w = max(300, SCR_W - 560)
    img_h = max(300, SCR_H - HEADER_H - 220)

    photo = load_image(animal["image_url"], (img_w, img_h))
    quiz_state["_current_photo"] = photo  # keep ref

    lbl_img = tk.Label(img_frame, image=photo, bg="#1a3a1a")
    lbl_img.pack(padx=4, pady=4)

    # Nom de l'animal
    tk.Label(col_left, text=animal["nom_commun"],
             font=NF, fg="#34c759", bg="#0a1a0a").pack(anchor="w")
    tk.Label(col_left, text=animal["nom_scientifique"],
             font=tkfont.Font(family="Courier New", size=12, slant="italic"),
             fg="#7aaa7a", bg="#0a1a0a").pack(anchor="w", pady=(2, 0))

    # ── Colonne droite ──
    tk.Label(col_right, text="CHOISISSEZ LA RÉGION",
             font=LF, fg="#34c759", bg="#0a1a0a").pack(pady=(20, 4))
    tk.Frame(col_right, bg="#34c759", height=1).pack(fill="x", pady=(0, 20))

    result_label = tk.Label(col_right, text="", font=MF,
                             bg="#0a1a0a", wraplength=400, justify="center")
    result_label.pack(pady=(0, 10))

    next_btn = tk.Button(col_right, text="", bg="#0a1a0a", fg="#0a1a0a",
                         font=LF, relief="flat", cursor="hand2",
                         padx=20, pady=8, state="disabled")

    btn_refs = []

    def on_answer(chosen_region, btn):
        if quiz_state["answered"]:
            return
        quiz_state["answered"] = True

        if chosen_region == correct_region:
            quiz_state["score"] += 1
            btn.configure(bg="#34c759", fg="#0a1a0a")
            result_label.configure(
                text=f"✓  Bonne réponse !\n{correct_region}",
                fg="#34c759", bg="#0a1a0a")
        else:
            btn.configure(bg="#e84040", fg="white")
            result_label.configure(
                text=f"✗  Mauvaise réponse…\nC'était : {correct_region}",
                fg="#e84040", bg="#0a1a0a")
            for b, r in btn_refs:
                if r == correct_region:
                    b.configure(bg="#34c759", fg="#0a1a0a")

        for b, r in btn_refs:
            b.configure(state="disabled")

        # Afficher le bouton suivant / résultat
        next_btn.configure(state="normal", fg="white")
        if idx + 1 < QUIZ_SIZE:
            next_btn.configure(
                text="Question suivante  ›",
                bg="#34c759", fg="#0a1a0a",
                command=lambda: [quiz_state.update({"current_index": idx + 1}),
                                 show_question()])
        else:
            next_btn.configure(
                text="Voir mon résultat  ›",
                bg="#d9c44a", fg="#0a1a0a",
                command=lambda: [quiz_state.update({"current_index": idx + 1}),
                                 show_results()])
        next_btn.pack(pady=(10, 0), fill="x", padx=10)

    # ── Boutons de réponse ──
    for region in options:
        col = REGION_COLORS.get(region, "#34c759")
        r_btn = tk.Button(col_right, text=region,
                          font=QF, bg="#0f2a0f", fg=col,
                          relief="flat", cursor="hand2",
                          padx=10, pady=10, wraplength=380,
                          anchor="w")
        r_btn.configure(command=lambda r=region, b=r_btn: on_answer(r, b))
        r_btn.pack(fill="x", padx=10, pady=5)

        def on_e(e, b=r_btn, c=col):
            if str(b["state"]) != "disabled":
                b.configure(bg=c, fg="#0a1a0a")

        def on_l(e, b=r_btn, c=col):
            if str(b["state"]) != "disabled" and b["bg"] not in ("#34c759", "#e84040"):
                b.configure(bg="#0f2a0f", fg=c)

        r_btn.bind("<Enter>", on_e)
        r_btn.bind("<Leave>", on_l)
        btn_refs.append((r_btn, region))

 # ── ECRAN DES RESULTATS ──

def show_results():
    for w in main_frame.winfo_children():
        w.destroy()

    score = quiz_state["score"]

    results = tk.Frame(main_frame, bg="#0a1a0a")
    results.pack(expand=True)

    tk.Label(results, text="🏆  Résultats",
             font=NF, fg="#34c759", bg="#0a1a0a").pack(pady=(40, 10))
    tk.Frame(results, bg="#34c759", height=1).pack(fill="x", padx=80, pady=(0, 30))

    # Score visuel
    score_color = "#34c759" if score >= 7 else "#d9c44a" if score >= 4 else "#e84040"

    tk.Label(results,
             text=f"{score}  /  {QUIZ_SIZE}",
             font=tkfont.Font(family="Courier New", size=60, weight="bold"),
             fg=score_color, bg="#0a1a0a").pack(pady=(10, 0))

    if score == 10:
        msg = "🌟  Parfait ! Vous êtes un expert de la faune mondiale !"
    elif score >= 7:
        msg = "🎉  Très bien ! Vous connaissez bien les animaux du monde."
    elif score >= 5:
        msg = "👍  Pas mal ! Quelques révisions sur la carte s'imposent."
    elif score >= 3:
        msg = "📚  Retournez explorer la carte pour progresser !"
    else:
        msg = "🗺️  La carte interactive est votre meilleure amie !"

    tk.Label(results, text=msg,
             font=MF, fg="#d4e8d4", bg="#0a1a0a",
             wraplength=600, justify="center").pack(pady=(10, 30))

    # Barre de score
    bar_frame = tk.Frame(results, bg="#1a3a1a", height=16, width=500)
    bar_frame.pack(pady=(0, 30))
    bar_frame.pack_propagate(False)
    fill_w = int(500 * score / QUIZ_SIZE)
    tk.Frame(bar_frame, bg=score_color, height=16, width=fill_w).place(x=0, y=0)

    # Boutons
    btn_row = tk.Frame(results, bg="#0a1a0a")
    btn_row.pack()

    replay_btn = tk.Button(btn_row, text="🔄  Rejouer",
                           bg="#34c759", fg="#0a1a0a", font=MF,
                           relief="flat", cursor="hand2", padx=30, pady=12,
                           command=start_quiz)
    replay_btn.pack(side="left", padx=20)

    carte_btn = tk.Button(btn_row, text="🗺️  Voir la carte",
                          bg="#4a90d9", fg="white", font=MF,
                          relief="flat", cursor="hand2", padx=30, pady=12,
                          command=lambda: [launch_script("carte.py"),
                                           sys.exit()])
    carte_btn.pack(side="left", padx=20)

    menu_btn = tk.Button(btn_row, text="🏠  Menu principal",
                         bg="#1a3a1a", fg="#34c759", font=MF,
                         relief="flat", cursor="hand2", padx=30, pady=12,
                         command=retour_menu)
    menu_btn.pack(side="left", padx=20)

    for btn, hov in [(replay_btn, "#57e87d"), (carte_btn, "#6aaae9"), (menu_btn, "#2a5a2a")]:
        orig = btn["bg"]
        btn.bind("<Enter>", lambda e, b=btn, h=hov: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, o=orig: b.configure(bg=o))

# ── RETOUR ECRAN D'ACCEUIL ──
show_home()

root.mainloop()
