import streamlit as st
import math
from PIL import Image

# --- Logo (opzionale) ---
try:
    logo = Image.open("logo.png")
    st.image(logo, width=100)
except:
    pass

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
    return math.floor(valore * 20) / 20.0

# --- UI Streamlit ---
st.set_page_config(page_title="Calcolo Booking", layout="centered")

st.title("🚗 Calcolo Booking")
st.markdown("Calcola il netto e confrontalo col costo del mezzo")

# --- Input Utente ---
veicolo = st.selectbox("Tipo veicolo", ["Standard/Berlina", "Van fino a 6 pax", "Van 7/8 pax"])
corsa = st.selectbox("Tipo servizio", ["Partenza", "Arrivo", "Spostamento", "Civitavecchia"])
notte = st.checkbox("Fascia notturna (22:00 - 05:59)")
prezzo_booking_input = st.text_input("Prezzo da Booking (€)", value="")

# --- Calcolo ---
if st.button("Calcola"):
    try:
        prezzo_booking = float(prezzo_booking_input.replace(",", "."))
        prezzo_mezzo = calcola_prezzo_mezzo(veicolo, corsa, notte)
        senza_iva, netto = calcola_netto_booking(prezzo_booking)
        netto_arrotondato = arrotonda_per_difetto_5cent(netto)

        st.markdown(f"**Senza IVA:** € {senza_iva:.2f}  \n**Netto:** € {netto:.2f}")

        highlight_style = "background-color: #f4c542; padding: 10px; border-radius: 8px;"

        if netto_arrotondato < prezzo_mezzo:
            st.markdown(
                f"<div style='{highlight_style}'>✔ Booking Netto: € {netto_arrotondato:.2f}<br>Costo Mezzo: € {prezzo_mezzo:.2f}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='{highlight_style}'>Booking Netto: € {netto_arrotondato:.2f}<br>✔ Costo Mezzo: € {prezzo_mezzo:.2f}</div>",
                unsafe_allow_html=True
            )

    except ValueError:
        st.error("Inserisci un numero valido per il prezzo Booking")
