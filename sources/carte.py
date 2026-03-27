import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw
import sqlite3
import os
import subprocess
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
ANIMAL_IMAGE_DIR = os.path.join(DATA_DIR, "animaux")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
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
MAP_FILE = os.path.join(IMAGE_DIR, "carte_monde.jpg")
LEG_W    = 220

# ── Positions des régions en % du canvas ──
# Calculées depuis coordonnées géographiques réelles
REGION_POS_PCT = {
    "Afrique":                     (0.535, 0.610),
    "Europe":                      (0.500, 0.390),
    "Asie":                        (0.700, 0.460),
    "Amérique du Nord":            (0.225, 0.330),
    "Amérique du Sud":             (0.350, 0.670),
    "Océanie":                     (0.800, 0.680),
    "Antarctique":                 (0.500, 0.880),
    "Moyen-Orient":                (0.580, 0.460),
    "Asie du Sud-Est":             (0.730, 0.560),
    "Caraïbes & Amérique Centrale":(0.278, 0.500),
}

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


# ── BASE DE DONNEES ──

def get_animaux_par_region(region_nom):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT e.*, r.nom_region, h.nom_habitat, ra.nom as regime
        FROM Especes e
        JOIN Regions r ON e.region_id = r.id
        JOIN Habitats h ON e.habitat_id = h.id
        JOIN RegimesAlimentaires ra ON e.regime_id = ra.id
        WHERE r.nom_region = ?
    """, (region_nom,))
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


# ── FENETRE FICHE ANIMAL ──

def ouvrir_detail_animal(animal, parent):
    win = tk.Toplevel(parent)
    win.title(animal["nom_commun"])
    win.geometry("900x900")
    win.configure(bg="#0a1a0a")
    win.grab_set()

    TF = tkfont.Font(family="Courier New", size=22, weight="bold")
    SF = tkfont.Font(family="Courier New",     size=13, slant="italic")
    LF = tkfont.Font(family="Courier New", size=11, weight="bold")
    VF = tkfont.Font(family="Courier New", size=11)
    DF = tkfont.Font(family="Courier New",     size=12)

    main = tk.Frame(win, bg="#0a1a0a")
    main.pack(fill="both", expand=True, padx=30, pady=20)

    col_left  = tk.Frame(main, bg="#0a1a0a")
    col_left.pack(side="left", fill="both", expand=True)
    col_right = tk.Frame(main, bg="#0a1a0a", width=300)
    col_right.pack(side="right", fill="y", padx=(20, 0))
    col_right.pack_propagate(False)

    img_frame = tk.Frame(col_right, bg="#1a3a1a")
    img_frame.pack(pady=(10, 0))
    photo = load_image(animal["image_url"], (280, 280))
    lbl = tk.Label(img_frame, image=photo, bg="#1a3a1a")
    lbl.image = photo
    lbl.pack(padx=4, pady=4)

    color = REGION_COLORS.get(animal["nom_region"], "#34c759")
    tk.Label(col_right, text=f"📍 {animal['nom_region']}",
             font=VF, fg=color, bg="#0a1a0a").pack(pady=(8, 0))

    tk.Label(col_left, text=animal["nom_commun"], font=TF,
             fg="#34c759", bg="#0a1a0a", anchor="w").pack(anchor="w", pady=(10, 0))
    tk.Label(col_left, text=animal["nom_scientifique"], font=SF,
             fg="#7aaa7a", bg="#0a1a0a", anchor="w").pack(anchor="w", pady=(2, 12))
    tk.Frame(col_left, bg="#34c759", height=1).pack(fill="x", pady=(0, 16))

    for label_txt, val in [
        ("🏔  Habitat",          animal["nom_habitat"]),
        ("🍽  Régime",           animal["regime"]),
        ("📏  Taille",           animal["taille_moyenne"]),
        ("⚖  Poids",            animal["poids_moyen"]),
        ("⏳  Espérance de vie", animal["esperance_vie"]),
        ("🔗  Niveau trophique", str(animal["niveau_trophique"])),
    ]:
        row = tk.Frame(col_left, bg="#0a1a0a")
        row.pack(anchor="w", fill="x", pady=3)
        tk.Label(row, text=f"{label_txt} :", font=LF,fg="#7aaa7a", bg="#0a1a0a", width=22, anchor="w").pack(side="left")
        tk.Label(row, text=val, font=VF,fg="white", bg="#0a1a0a", anchor="w").pack(side="left")

    tk.Frame(col_left, bg="#1a3a1a", height=1).pack(fill="x", pady=(14, 10))
    tk.Label(col_left, text="Description", font=LF,fg="#7aaa7a", bg="#0a1a0a", anchor="w").pack(anchor="w")
    tk.Label(col_left, text=animal["description"], font=DF,fg="#d4e8d4", bg="#0a1a0a", wraplength=480,justify="left", anchor="w").pack(anchor="w", pady=(6, 0))

    tk.Button(win, text="✕  Fermer", command=win.destroy,bg="#34c759", fg="#0a1a0a", font=LF,relief="flat", cursor="hand2", padx=20, pady=8).pack(pady=14)


# ── FENETRE ANIMAUX REGIONS ──

def ouvrir_region(region_nom, root_win):
    animaux = get_animaux_par_region(region_nom)
    if not animaux:
        return

    win = tk.Toplevel(root_win)
    win.title(f"Animaux — {region_nom}")
    win.geometry("1500x800")
    win.configure(bg="#0a1a0a")
    win.grab_set()

    TF    = tkfont.Font(family="Courier New", size=18, weight="bold")
    NF    = tkfont.Font(family="Courier New", size=10, weight="bold")
    color = REGION_COLORS.get(region_nom, "#34c759")

    hdr = tk.Frame(win, bg="#0a1a0a")
    hdr.pack(fill="x", padx=30, pady=(20, 10))
    tk.Label(hdr, text=f"🌍  {region_nom}", font=TF,
             fg=color, bg="#0a1a0a").pack(side="left")
    tk.Button(hdr, text="✕", command=win.destroy,
              bg="#1a3a1a", fg=color, font=TF,
              relief="flat", cursor="hand2", padx=10).pack(side="right")
    tk.Frame(win, bg=color, height=2).pack(fill="x", padx=30, pady=(0, 16))

    cl = tk.Canvas(win, bg="#0a1a0a", highlightthickness=0)
    sb = tk.Scrollbar(win, orient="vertical", command=cl.yview)
    cl.configure(yscrollcommand=sb.set)
    cl.pack(side="left",  fill="both", expand=True, padx=(30, 0), pady=(0, 20))
    sb.pack(side="right", fill="y",    pady=(0, 20), padx=(0, 10))

    gf = tk.Frame(cl, bg="#0a1a0a")
    cl.create_window((0, 0), window=gf, anchor="nw")

    img_refs = []

    for idx, animal in enumerate(animaux):
        ri, ci = divmod(idx, 5)

        cell = tk.Frame(gf, bg="#0f2a0f", cursor="hand2", width=240, height=260)
        cell.grid(row=ri, column=ci, padx=15, pady=15)
        cell.pack_propagate(False)  

        photo = load_image(animal["image_url"], (220, 190))
        img_refs.append(photo)

        il = tk.Label(cell, image=photo, bg="#0f2a0f", cursor="hand2")
        il.image = photo
        il.pack(padx=4, pady=(4, 0))

        nl = tk.Label(cell, text=animal["nom_commun"], font=NF,
                  fg=color, bg="#0f2a0f", wraplength=210, justify="center")
        nl.pack(padx=4, pady=(2, 4))

        def on_click(e, a=animal): ouvrir_detail_animal(a, win)

        def on_enter(e, f=cell, c=color):
            f.configure(bg=c)
            for ch in f.winfo_children(): ch.configure(bg=c)

        def on_leave(e, f=cell):
            f.configure(bg="#0f2a0f")
            for ch in f.winfo_children(): ch.configure(bg="#0f2a0f")

        for w in (cell, il, nl):
            w.bind("<Button-1>", on_click)
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)

    gf.update_idletasks()
    cl.configure(scrollregion=cl.bbox("all"))
    win._img_refs = img_refs


# ── FENETRE PRINCIPALE ──

ensure_database()

root = tk.Tk()
root.title("Nature Atlas — Carte du Monde")
root.configure(bg="#09471c")

root.state('zoomed')
root.update_idletasks()
SCR_W = root.winfo_screenwidth()
SCR_H = root.winfo_screenheight()

HEADER_H = 82
CANVAS_H  = SCR_H - HEADER_H - 4
CANVAS_W  = SCR_W - LEG_W

# Polices
TF  = tkfont.Font(family="Courier New", size=22, weight="bold")
SF  = tkfont.Font(family="Courier New", size=11, slant="italic")
BF  = tkfont.Font(family="Courier New", size=10, weight="bold")
LTF = tkfont.Font(family="Courier New", size=10, weight="bold")
LIF = tkfont.Font(family="Courier New", size=9)

# ── EN-TÊTE ──

hdr = tk.Frame(root, bg="#09471c", height=HEADER_H)
hdr.pack(fill="x", side="top")
hdr.pack_propagate(False)

tk.Label(hdr, text="Nature Atlas",font=TF, fg="white", bg="#09471c").pack(pady=(12, 2))
tk.Label(hdr, text="Cliquez sur une région pour découvrir ses animaux",font=SF, fg="#a8d8a8", bg="#09471c").pack()
tk.Frame(hdr, bg="lightgreen", height=2).pack(fill="x", padx=60, pady=(5, 0))

# ── CORPS ──
body = tk.Frame(root, bg="#09471c")
body.pack(fill="both", expand=True)

# ── PANNEAU LÉGENDE ──
leg = tk.Frame(body, bg="#0a1a0a", width=LEG_W)
leg.pack(side="left", fill="y")
leg.pack_propagate(False)

tk.Label(leg, text="RÉGIONS DU MONDE",font=LTF, fg="#34c759", bg="#0a1a0a").pack(pady=(18, 6))
tk.Frame(leg, bg="#34c759", height=1).pack(fill="x", padx=14, pady=(0, 8))

for region, col in REGION_COLORS.items():
    row = tk.Frame(leg, bg="#0a1a0a", cursor="hand2")
    row.pack(fill="x", padx=14, pady=4)

    dot = tk.Canvas(row, width=14, height=14, bg="#0a1a0a", highlightthickness=0)
    dot.pack(side="left", padx=(0, 6))
    dot.create_oval(1, 1, 13, 13, fill=col, outline="")

    txt = region[:22] + ("…" if len(region) > 22 else "")
    lbl = tk.Label(row, text=txt, font=LIF, fg="white",
                   bg="#0a1a0a", anchor="w")
    lbl.pack(side="left")

    def on_click_leg(e, r=region): ouvrir_region(r, root)

    def on_enter_leg(e, f=row, c=col):
        f.configure(bg=c)
        for ch in f.winfo_children(): ch.configure(bg=c)

    def on_leave_leg(e, f=row):
        f.configure(bg="#0a1a0a")
        for ch in f.winfo_children(): ch.configure(bg="#0a1a0a")

    for w in (row, lbl, dot):
        w.bind("<Button-1>", on_click_leg)
        w.bind("<Enter>",    on_enter_leg)
        w.bind("<Leave>",    on_leave_leg)

# ── CANVAS CARTE ──

canvas = tk.Canvas(body, width=CANVAS_W, height=CANVAS_H,bg="#0b1f2e", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# ── CHARGEMENT CARTE ──

if os.path.exists(MAP_FILE):
    map_img   = Image.open(MAP_FILE).convert("RGB")
    map_img   = map_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    map_photo = ImageTk.PhotoImage(map_img)
    canvas._map_photo = map_photo
    canvas.create_image(0, 0, anchor="nw", image=map_photo)
else:
    canvas.create_text(CANVAS_W // 2, CANVAS_H // 2,text=f"Fichier '{MAP_FILE}' introuvable.\nPlacez-le dans le dossier du projet.",fill="#e84040", font=("Courier New", 14, "bold"), justify="center")

# ── BOUTONS RÉGIONS ──
R_OUT = 22  
R_IN  = 14   

for region, (px, py) in REGION_POS_PCT.items():
    cx = int(px * CANVAS_W)
    cy = int(py * CANVAS_H)
    col = REGION_COLORS[region]

    canvas.create_oval(cx - R_OUT, cy - R_OUT, cx + R_OUT, cy + R_OUT,
                       fill="", outline=col, width=2)

    canvas.create_oval(cx - R_IN, cy - R_IN, cx + R_IN, cy + R_IN,
                       fill=col, outline="white", width=1)

    short = region.replace("Caraïbes & Amérique Centrale", "Caraïbes &\nAmér. Centrale")
    canvas.create_text(cx + 1, cy + R_OUT + 12, text=short,
                       fill="black", font=("Courier New", 7, "bold"), justify="center")
    canvas.create_text(cx,     cy + R_OUT + 11, text=short,
                       fill="white", font=("Courier New", 7, "bold"), justify="center")

    btn = tk.Button(
        canvas, text="", bg=col,
        activebackground="white", relief="flat",
        cursor="hand2", bd=0,
        command=lambda r=region: ouvrir_region(r, root)
    )
    canvas.create_window(cx, cy, window=btn, width=28, height=28)

    def make_tt(r, c, bx, by):
        tip = [None]
        def show(e, region=r, color=c, x=bx, y=by):
            tip[0] = canvas.create_text(
                x, y - 34,
                text=f"✦ {region}",
                fill=color,
                font=("Courier New", 9, "bold")
            )
        def hide(e):
            if tip[0]:
                canvas.delete(tip[0])
                tip[0] = None
        return show, hide

    sf, hf = make_tt(region, col, cx, cy)
    btn.bind("<Enter>", sf)
    btn.bind("<Leave>", hf)

# ── BOUTON RETOUR MENU ──
def retour_menu():
    launch_script("Index.py")
    sys.exit()

btn_frame = tk.Frame(root, bg="black", width=220, height=34)
btn_frame.place(x=4, y=4)
tk.Button(btn_frame, text="<<< Retourner au menu",
          bg="#34c759", fg="white", font=BF,
          relief="flat", cursor="hand2",
          command=retour_menu).pack(expand=True, fill="both")

root.mainloop()
