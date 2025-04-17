import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import os
import sys

# --- Funzioni utili per risorse ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Funzioni di calcolo ---
def calcola_prezzo_mezzo(veicolo, corsa, notte):
    prezzi = {
        "Standard/Berlina": {"Partenza": 50, "Arrivo": 55, "Spostamento": 30, "Civitavecchia": 120},
        "Van fino a 6 pax": {"Partenza": 55, "Arrivo": 60, "Spostamento": 40, "Civitavecchia": 140},
        "Van 7/8 pax": {"Partenza": 60, "Arrivo": 65, "Spostamento": 45, "Civitavecchia": 150}
    }
    base = prezzi[veicolo][corsa]
    if notte:
        base += 10 if corsa == "Civitavecchia" else 5
    return base

def calcola_netto_booking(prezzo_booking):
    senza_iva = prezzo_booking / 1.1
    netto = senza_iva / 1.05
    return senza_iva, netto

def arrotonda_per_difetto_5cent(valore):
    return math.floor(valore * 20) / 20

def calcola(event=None):
    try:
        prezzo_booking = float(entry_booking.get().replace(",", "."))
        veicolo = combo_veicolo.get()
        corsa = combo_corsa.get()
        notte = notte_var.get()

        prezzo_mezzo = calcola_prezzo_mezzo(veicolo, corsa, notte)
        senza_iva, netto = calcola_netto_booking(prezzo_booking)
        netto_arrotondato = arrotonda_per_difetto_5cent(netto)

        label_risultato.config(text=f"\nSenza IVA: € {senza_iva:.2f}\nNetto: € {netto:.2f}", font=("Segoe UI", 9))

        confronto_label_frame.pack(pady=10)

        highlight_color = "#f4c542"

        if netto_arrotondato < prezzo_mezzo:
            confronto_label.config(
                text=f"✔ Booking Netto: € {netto_arrotondato:.2f}\nCosto Mezzo: € {prezzo_mezzo:.2f}",
                font=("Segoe UI", 11, "bold"),
                foreground=highlight_color
            )
        else:
            confronto_label.config(
                text=f"Booking Netto: € {netto_arrotondato:.2f}\n✔ Costo Mezzo: € {prezzo_mezzo:.2f}",
                font=("Segoe UI", 11, "bold"),
                foreground=highlight_color
            )

    except ValueError:
        messagebox.showerror("Errore", "Inserisci un numero valido per il prezzo Booking")

# --- UI Setup ---
root = ttk.Window(themename="darkly")
root.title("Calcolo Booking")
root.geometry("460x660")

try:
    root.iconbitmap(resource_path("logo.ico"))
except:
    pass

# --- Font ---
font_titolo = ("Segoe UI", 16, "bold")
font_label = ("Segoe UI", 10)
font_valori = ("Segoe UI", 12, "bold")

# --- Logo ---
try:
    img = Image.open(resource_path("logo.png"))
    img = img.resize((100, 100))
    logo_img = ImageTk.PhotoImage(img)
    ttk.Label(root, image=logo_img).pack(pady=5)
except:
    pass

# --- Titolo ---
ttk.Label(root, text="Calcolo Booking", font=font_titolo, foreground="#f4c542").pack(pady=5)

frame = ttk.Frame(root)
frame.pack(pady=10)

# --- Selezioni ---
ttk.Label(frame, text="Tipo veicolo", font=font_label, foreground="#f4c542").grid(row=0, column=0, sticky="w")
combo_veicolo = ttk.Combobox(frame, values=["Standard/Berlina", "Van fino a 6 pax", "Van 7/8 pax"], width=25)
combo_veicolo.set("Standard/Berlina")
combo_veicolo.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame, text="Tipo servizio", font=font_label, foreground="#f4c542").grid(row=1, column=0, sticky="w")
combo_corsa = ttk.Combobox(frame, values=["Partenza", "Arrivo", "Spostamento", "Civitavecchia"], width=25)
combo_corsa.set("Partenza")
combo_corsa.grid(row=1, column=1, padx=10, pady=5)

notte_var = ttk.BooleanVar()
ttk.Checkbutton(frame, text="Fascia notturna (22:00 - 05:59)", variable=notte_var, bootstyle="success-round-toggle").grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

# --- Prezzo Booking ---
ttk.Label(root, text="Prezzo da Booking (€)", font=font_label, foreground="#f4c542").pack()
entry_booking = ttk.Entry(root, font=font_label, width=20, justify="center")
entry_booking.pack(pady=5)
entry_booking.bind("<Return>", calcola)

# --- Bottone ---
ttk.Button(root, text="Calcola", command=calcola, bootstyle="warning-outline").pack(pady=10)

# --- Risultati ---
label_risultato = ttk.Label(root, text="", font=("Segoe UI", 9), justify="left", foreground="#f4c542")
label_risultato.pack()

confronto_label_frame = ttk.Frame(root)
confronto_label = ttk.Label(confronto_label_frame, text="", font=("Segoe UI", 11), justify="left", wraplength=420)
confronto_label.pack()

root.mainloop()
