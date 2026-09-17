import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="FanRadar Planspiel", layout="wide")

# --- 1. GAME STATE INITIALISIERUNG ---
if 'saison' not in st.session_state:
    st.session_state.saison = 1
    st.session_state.max_saisons = 4
    st.session_state.budget = 250000
    st.session_state.history = []
    st.session_state.game_finished = False

# --- 2. KOPFZEILE & FORTSCHRITT ---
st.title("⚽ FanRadar: Strategisches Vereins-Planspiel")

if st.session_state.game_finished:
    st.success("🎉 **Planspiel abgeschlossen!** Hier ist deine Bilanz über 4 Saisons:")
    
    df_res = pd.DataFrame(st.session_state.history)
    st.dataframe(df_res, use_container_width=True)
    
    fig = px.line(df_res, x="Saison", y=["Umsatz (€)", "Gesamtbudget (€)"], markers=True, title="Entwicklung über die Jahre")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔄 Neues Spiel starten"):
        st.session_state.saison = 1
        st.session_state.budget = 250000
        st.session_state.history = []
        st.session_state.game_finished = False
        st.rerun()
    st.stop()

# Status-Display
col_stat1, col_stat2, col_stat3 = st.columns(3)
col_stat1.metric("Aktuelle Runde", f"Saison {st.session_state.saison} von {st.session_state.max_saisons}")
col_stat2.metric("Verfügbares Budget", f"{int(st.session_state.budget):,} €".replace(",", "."))
col_stat3.progress(st.session_state.saison / st.session_state.max_saisons, text="Saison-Fortschritt")

st.markdown("---")

# --- 3. EREIGNIS/SZENARIO FÜR DIE AKTUELLE RUONDE ---
szenarien = {
    1: "📌 **Saison 1 - Basis-Positionierung:** Lege die Grundlagen für Preissetzung, Fan-Akquise und Sponsoring fest.",
    2: "🏆 **Saison 2 - Frauen-EM Hype:** Das Interesse an Frauenfußball steigt stark an. Equal-Pay-Initiativen wirken dieses Jahr besonders stark.",
    3: "📉 **Saison 3 - Preissensibilität & Inflation:** Die Fans reagieren empfindlicher auf Preiserhöhungen im Männerbereich.",
    4: "⚡ **Saison 4 - Sponsoren-Entscheidung:** Dein Hauptsponsor verlangt klare Ergebnisse bei Reichweite oder Nachhaltigkeit."
}

st.info(szenarien[st.session_state.saison])

# --- 4. RUNDEN-EINSTELLUNGEN (DEIN UI-DESIGN) ---
st.subheader(f"⚙️ Stellschrauben für Saison {st.session_state.saison}")

col1, col2 = st.columns(2)

with col1:
    zielgruppe_groesse = st.slider("Zielgruppen-Reichweite (Marketing-Investment)", 1, 10, 3, help="Bestimmt den Aufwand für Fan-Akquise")
    anteil_leistungssport = st.slider("Anteil Frauenfußball-Investment (%)", 0, 50, 15, help="Prozentualer Re-Investment-Satz")

with col2:
    einteilung_sorgfalt = st.select_slider(
        "Aktivierungs-Fokus", 
        options=["Pragmatisch (Wenig Aufwand)", "Balanced", "Perfekt Segmentiert (Hohe Kosten)"],
        help="Tiefe der Fan-Segmentierung"
    )
    preis_ticket = st.slider("Preis pro Ticket / Stunde (€)", 15, 60, 30)

st.markdown("---")

# --- 5. RUONDEN-BUTTON (EXAKT WIE AUF DEINEM SCREENSHOT) ---
button_label = f"⏩ Jahr {st.session_state.saison} simulieren"

if st.button(button_label, type="primary"):
    # BERECHNUNG DER RUONDE
    marketing_cost = zielgruppe_groesse * 15000
    segmentation_cost = {"Pragmatisch (Wenig Aufwand)": 5000, "Balanced": 15000, "Perfekt Segmentiert (Hohe Kosten)": 35000}[einteilung_sorgfalt]
    
    # Formel für Einnahmen basierend auf Runden-Variablen
    base_demand = (100 - preis_ticket) * 150
    hype_factor = 1.5 if st.session_state.saison == 2 else 1.0
    
    revenue = (base_demand * preis_ticket * (1 + anteil_leistungssport / 100)) * hype_factor
    profit = revenue - (marketing_cost + segmentation_cost)
    
    # BUDGET UPDATEN
    st.session_state.budget += profit
    
    # HISTORIE SPEICHERN
    st.session_state.history.append({
        "Saison": f"Jahr {st.session_state.saison}",
        "Ticketpreis (€)": preis_ticket,
        "Umsatz (€)": revenue,
        "Gewinn/Verlust (€)": profit,
        "Gesamtbudget (€)": st.session_state.budget
    })
    
    # WEITERZÄHLEN ODER BEENDEN
    if st.session_state.saison < st.session_state.max_saisons:
        st.session_state.saison += 1
    else:
        st.session_state.game_finished = True
        
    st.rerun()

# --- 6. BISHERIGER VERLAUF (TABELLE DARUNTER) ---
if st.session_state.history:
    st.subheader("📋 Bisherige Saisonergebnisse")
    st.table(pd.DataFrame(st.session_state.history))
