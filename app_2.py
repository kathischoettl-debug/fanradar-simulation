import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="FanRadar Turn-Based Engine", layout="wide")

# --- 1. SICHERE INITIALISIERUNG (VERHINDERT KEYERROR) ---
def init_game_state():
    default_values = {
        'saison': 1,
        'max_saisons': 4,
        'budget': 250000,
        'fans_tradition': 5000,
        'fans_opp': 3000,
        'fans_values': 2000,
        'history': [],
        'game_finished': False
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_game_state()

# --- 2. HEADER & GAME OVER ---
st.title("⚽ FanRadar: Strategisches Vereins-Planspiel")

if st.session_state.game_finished:
    st.balloons()
    st.success("🎉 **Planspiel abgeschlossen!** Hier ist deine 4-Jahres-Bilanz:")
    
    df_res = pd.DataFrame(st.session_state.history)
    st.dataframe(df_res, use_container_width=True)
    
    fig = px.line(df_res, x="Saison", y=["Gesamtertrag (€)", "Klub-Budget (€)", "Gesamt-Fans"], markers=True, title="Entwicklung über 4 Saisons")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔄 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_game_state()
        st.rerun()
    st.stop()

# Dashboard Top-Metrics (Sichere Formatierung)
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Aktuelle Runde", f"Saison {st.session_state.saison} / {st.session_state.max_saisons}")
m2.metric("Klub-Budget", f"{int(st.session_state.budget):,} €".replace(",", "."))
m3.metric("Traditions-Fans", f"{int(st.session_state.fans_tradition):,}".replace(",", "."))
m4.metric("Opportunisten", f"{int(st.session_state.fans_opp):,}".replace(",", "."))
m5.metric("Werte-Fans", f"{int(st.session_state.fans_values):,}".replace(",", "."))

st.progress(st.session_state.saison / st.session_state.max_saisons)
st.markdown("---")

# --- 3. EREIGNIS FÜR DIE RUONDE ---
szenarien = {
    1: "📌 **Saison 1 - Basis-Positionierung:** Lege die Grundlagen für Preissetzung, Fan-Akquise und Sponsoring fest.",
    2: "🏆 **Saison 2 - Frauen-EM Hype:** Das Interesse an Frauenfußball steigt bundesweit. Equal-Pay- und Werte-Initiativen wirken dieses Jahr doppelt stark!",
    3: "📉 **Saison 3 - Preissensibilität & Inflation:** Die Fans achten strenger auf ihr Geld. Preiserhöhungen führen zu stärkere Churn.",
    4: "⚡ **Saison 4 - Hauptsponsor-Entscheidung:** Dein Hauptsponsor stellt Forderungen: Hohe Reichweite oder maximale Nachhaltigkeit."
}

st.info(szenarien.get(st.session_state.saison, "Saison läuft..."))
st.subheader(f"⚙️ Management-Stellschrauben für Saison {st.session_state.saison}")

# --- 4. VOLLES VARIABLEN-SET ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**1. Akquise & Segmentierung**")
    max_acq = max(10000, int(st.session_state.budget))
    acq_budget = st.slider("Akquise-Budget (€)", 10000, min(100000, max_acq), 30000, step=5000)
    acq_focus = st.selectbox("Akquise-Kanal / Zielgruppe", ["Breitensport & Nachwuchs", "Performance & Social Media", "Equal Pay & Werte-Kommunikation"])
    segmentation_depth = st.select_slider("Einteilungs-Sorgfalt (Fan-Profiling)", options=["Pragmatisch (Geringe Kosten)", "Balanced", "Perfekt Segmentiert (Hohe Kosten)"])

with col2:
    st.markdown("**2. Pricing & Stadion**")
    price_m = st.slider("Ticketpreis Männer (€)", 15, 60, 30)
    price_w = st.slider("Ticketpreis Frauen (€)", 5, 30, 10)
    merch_type = st.select_slider("Merchandising-Ausrichtung", options=["Standard", "Premium & Sustainable"])

with col3:
    st.markdown("**3. Sponsoring & Equal Pay**")
    sponsor_type = st.selectbox("Hauptsponsor-Profil", ["Regionaler Mittelstand (500k €)", "Wettanbieter / Krypto (900k €)", "Nachhaltigkeits-Brand (650k €)"])
    equal_pay_reinvest = st.slider("Equal Pay Re-Investment (%)", 0, 50, 15, help="% des Merch-Umsatzes fließen direkt in den Frauenfußball")

st.markdown("---")

# --- 5. SIMULATIONS-BUTTON UND BERECHNUNG ---
if st.button(f"⏩ Saison {st.session_state.saison} simulieren", type="primary"):
    
    seg_cost = {"Pragmatisch (Geringe Kosten)": 5000, "Balanced": 15000, "Perfekt Segmentiert (Hohe Kosten)": 35000}[segmentation_depth]
    seg_efficiency = {"Pragmatisch (Geringe Kosten)": 0.8, "Balanced": 1.0, "Perfekt Segmentiert (Hohe Kosten)": 1.3}[segmentation_depth]
    
    hype = 2.0 if (st.session_state.saison == 2 and acq_focus == "Equal Pay & Werte-Kommunikation") else 1.0
    
    if acq_focus == "Breitensport & Nachwuchs":
        d_trad = int((acq_budget / 8) * seg_efficiency)
        d_opp = int(acq_budget / 20)
        d_val = int(acq_budget / 30)
    elif acq_focus == "Performance & Social Media":
        d_trad = int(acq_budget / 40)
        d_opp = int((acq_budget / 6) * seg_efficiency * hype)
        d_val = int(acq_budget / 20)
    else:
        d_trad = int(acq_budget / 30)
        d_opp = int(acq_budget / 25)
        d_val = int((acq_budget / 5) * seg_efficiency * hype)

    inflation_factor = 1.4 if st.session_state.saison == 3 else 1.0
    
    visits_trad_m = max(2, int(14 - (price_m - 20) * 0.3 * inflation_factor))
    visits_opp_m = max(1, int(8 - (price_m - 30) * 0.2))
    
    sponsor_mult = 1.4 if sponsor_type == "Nachhaltigkeits-Brand (650k €)" else (0.3 if sponsor_type == "Wettanbieter / Krypto (900k €)" else 1.0)
    visits_val_w = max(1, int((6 + equal_pay_reinvest * 0.2) * sponsor_mult))
    visits_val_m = max(1, int((5 + equal_pay_reinvest * 0.1) * sponsor_mult))

    sponsorship_rev = {"Regionaler Mittelstand (500k €)": 500000, "Wettanbieter / Krypto (900k €)": 900000, "Nachhaltigkeits-Brand (650k €)": 650000}[sponsor_type]
    merch_spend = 35 if merch_type == "Premium & Sustainable" else 20
    
    rev_tickets_m = (st.session_state.fans_tradition * visits_trad_m + st.session_state.fans_opp * visits_opp_m + st.session_state.fans_values * visits_val_m) * price_m
    rev_tickets_w = (st.session_state.fans_values * visits_val_w + 1200) * price_w
    rev_merch = (st.session_state.fans_tradition + st.session_state.fans_opp + st.session_state.fans_values) * merch_spend
    
    rev_total = rev_tickets_m + rev_tickets_w + rev_merch + sponsorship_rev
    exp_total = acq_budget + seg_cost + 350000
    profit = rev_total - exp_total
    
    st.session_state.fans_tradition += d_trad
    st.session_state.fans_opp += d_opp
    st.session_state.fans_values += d_val
    st.session_state.budget += profit
    
    st.session_state.history.append({
        "Saison": f"Jahr {st.session_state.saison}",
        "Ticket Preis M/F (€)": f"{price_m} / {price_w}",
        "Gesamtertrag (€)": rev_total,
        "Gewinn (€)": profit,
        "Klub-Budget (€)": st.session_state.budget,
        "Gesamt-Fans": st.session_state.fans_tradition + st.session_state.fans_opp + st.session_state.fans_values
    })
    
    if st.session_state.saison < st.session_state.max_saisons:
        st.session_state.saison += 1
    else:
        st.session_state.game_finished = True
        
    st.rerun()

# --- 6. HISTORIE-TABELLE ---
if st.session_state.history:
    st.subheader("📋 Verlauf bisheriger Saisons")
    st.table(pd.DataFrame(st.session_state.history))
