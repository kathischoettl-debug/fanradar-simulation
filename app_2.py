import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="FanRadar Simulation Engine", layout="wide")

# --- 1. INITIALISIERUNG DER EMPIRISCHEN CLUSTER & ZUSTÄNDE ---
def init_game_state():
    default_values = {
        'saison': 1,
        'max_saisons': 4,
        'budget': 250000,
        # Die 4 empirischen Sozialisations-Cluster
        'cluster_social_local': 1065,
        'cluster_broadly_socialized': 882,
        'cluster_media_socialized': 885,
        'cluster_low_pathway': 747,
        'history': [],
        'game_finished': False
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_game_state()

# --- 2. HEADER & SPIELENDE ---
st.title("⚽ FanRadar: Strategisches Vereins-Planspiel")

if st.session_state.game_finished:
    st.balloons()
    st.success("🎉 **4-Jahres-Planspiel abgeschlossen!** Bilanz deines Managements:")
    
    df_res = pd.DataFrame(st.session_state.history)
    st.dataframe(df_res, use_container_width=True)
    
    fig = px.line(df_res, x="Saison", y=["Gesamtertrag (€)", "Klub-Budget (€)", "Gesamte Fanbase"], markers=True, title="Entwicklung der Kennzahlen über 4 Saisons")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔄 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_game_state()
        st.rerun()
    st.stop()

# --- DASHBOARD KPI METRICS ---
total_fans = (st.session_state.cluster_social_local + st.session_state.cluster_broadly_socialized + 
              st.session_state.cluster_media_socialized + st.session_state.cluster_low_pathway)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Aktuelle Runde", f"Saison {st.session_state.saison} / {st.session_state.max_saisons}")
m2.metric("Klub-Budget", f"{int(st.session_state.budget):,} €".replace(",", "."))
m3.metric("Social-Local", f"{int(st.session_state.cluster_social_local):,}")
m4.metric("Broadly Socialized", f"{int(st.session_state.cluster_broadly_socialized):,}")
m5.metric("Media-Socialized", f"{int(st.session_state.cluster_media_socialized):,}")
m6.metric("Low-Pathway", f"{int(st.session_state.cluster_low_pathway):,}")

st.progress(st.session_state.saison / st.session_state.max_saisons)
st.markdown("---")

# --- 3. EXTERNE SZENARIEN & SCHOCKS (DATENBASIERT) ---
szenarien = {
    1: "📌 **Saison 1 - Touchpoint-Aufbau:** Baue die Fanbase über gezielte Kontaktpunkte (Medien, Region, Fankultur) auf.",
    2: "⚠️ **Saison 2 - Finanzielle Notlage (1860-Szenario):** Der Klub benötigt außerordentliche Unterstützung zur Lizenzsicherung. Deine hoch gebundenen Cluster entscheiden über das Überleben!",
    3: "⚖️ **Saison 3 - Equal Pay & SWO-Debatte:** Soll ein Aufschlag auf Tickets zur Förderung der Geschlechtergerechtigkeit eingeführt werden? (Zahlungsbereitschaft liegt empirisch bei 36,4 %).",
    4: "⚡ **Saison 4 - Sponsoren-Ausrichtung:** Ein Großsponsor knüpft sein Investment an die Bindungsfrequenz deiner Stadionbesucher."
}

st.info(szenarien.get(st.session_state.saison, "Saison läuft..."))
st.subheader(f"⚙️ Management-Stellschrauben für Saison {st.session_state.saison}")

# --- 4. STELLSCHRAUBEN & STRATEGIE-VARIABLEN ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**1. Marketing & Touchpoint-Investition**")
    max_acq = max(10000, int(st.session_state.budget))
    marketing_budget = st.slider("Marketing-Budget (€)", 10000, min(100000, max_acq), 30000, step=5000)
    touchpoint_focus = st.selectbox(
        "Fokus-Sozialisationsweg", 
        [
            "Lokale & Soziale Wege (Familie, Region, Stadion)", 
            "Mediale Wege (Social Media, Live-Streaming, Web)", 
            "Organisierte Fankultur (Fanclubs, Stammtische)"
        ]
    )

with col2:
    st.markdown("**2. Pricing & Ticket-Struktur**")
    price_ticket = st.slider("Standard Ticketpreis (€)", 15, 60, 30)
    equal_pay_surcharge = st.slider("Equal-Pay Aufschlag auf Tageskarten (€)", 0, 10, 0, help="36,4% Akzeptanz in der Gesamtfanbase; hohe Akzeptanz bei SWO-Segmenten")

with col3:
    st.markdown("**3. Werte-Positionierung (SWO)**")
    swo_strategy = st.selectbox(
        "Gender Equity & SWO-Kommunikation", 
        [
            "Fokus Sport & Leistung (Klassisch)", 
            "Aktive SWO & Gender Equity Initiative (Prospektiv)"
        ]
    )
    sponsoring_type = st.selectbox(
        "Hauptsponsor", 
        ["Regionaler Mittelstand (500k €)", "Wettanbieter / Krypto (850k €)", "Nachhaltigkeits-Brand (600k €)"]
    )

st.markdown("---")

# --- 5. RUONDEN-SIMULATION (DATENBASIERTE CALCULATIONS) ---
if st.button(f"⏩ Saison {st.session_state.saison} simulieren", type="primary"):
    
    # --- A. SOZIALISATIONSEFFEKTE (TOUCHPOINT-INVESTMENTS) ---
    if "Lokale & Soziale" in touchpoint_focus:
        d_social_local = int(marketing_budget / 10)
        d_broadly = int(marketing_budget / 20)
        d_media = int(marketing_budget / 50)
        d_low = 0
    elif "Mediale Wege" in touchpoint_focus:
        d_social_local = int(marketing_budget / 50)
        d_broadly = int(marketing_budget / 30)
        d_media = int(marketing_budget / 8)
        d_low = int(marketing_budget / 40)
    else: # Organisierte Fankultur
        d_social_local = int(marketing_budget / 25)
        d_broadly = int(marketing_budget / 12)
        d_media = int(marketing_budget / 60)
        d_low = 0

    # --- B. STADIONBESUCHE (EMPIRISCHE GEMITTELTE BESUCHS-FREQUENZEN) ---
    # Social-Local: 6.13 | Broadly: 6.65 | Media: 2.76 | Low-Pathway: 2.79
    # Preissensibilität
    price_penalty = max(0.5, 1.0 - (price_ticket - 30) * 0.015)
    
    visits_social_local = 6.13 * price_penalty
    visits_broadly = 6.65 * price_penalty
    visits_media = 2.76 * price_penalty
    visits_low = 2.79 * price_penalty
    
    # Ticket-Einnahmen
    effective_ticket_price = price_ticket + equal_pay_surcharge
    
    # Akzeptanz des Equal-Pay Aufschlags
    surcharge_accept_rate = 0.364 if equal_pay_surcharge > 0 else 1.0
    if swo_strategy == "Aktive SWO & Gender Equity Initiative (Prospektiv)":
        surcharge_accept_rate += 0.15 # SWO Booster
        
    revenue_tickets = (
        (st.session_state.cluster_social_local * visits_social_local +
         st.session_state.cluster_broadly_socialized * visits_broadly +
         st.session_state.cluster_media_socialized * visits_media +
         st.session_state.cluster_low_pathway * visits_low) * effective_ticket_price * surcharge_accept_rate
    )
    
    # --- C. EXTERNE SZENARIEN & NOTHILFE (SAISON 2) ---
    nothilfe_donations = 0
    if st.session_state.saison == 2:
        # Nothilfe-Bereitschaft: Broadly 76.2%, Social-Local 61.2%, Media 58.8%, Low 46.0%
        nothilfe_donations = (
            (st.session_state.cluster_broadly_socialized * 0.762 * 50) +
            (st.session_state.cluster_social_local * 0.612 * 35) +
            (st.session_state.cluster_media_socialized * 0.588 * 20) +
            (st.session_state.cluster_low_pathway * 0.460 * 10)
        )
        st.toast(f"🚨 Nothilfe-Kampagne generierte {int(nothilfe_donations):,} € Spenden aus der Fanbase!")

    # --- D. SPONSORING & FIXKOSTEN ---
    sponsor_rev = {"Regionaler Mittelstand (500k €)": 500000, "Wettanbieter / Krypto (850k €)": 850000, "Nachhaltigkeits-Brand (600k €)": 600000}[sponsoring_type]
    
    rev_total = revenue_tickets + sponsor_rev + nothilfe_donations
    exp_total = marketing_budget + 300000  # Fixkosten
    profit = rev_total - exp_total
    
    # --- STATE UPDATE ---
    st.session_state.cluster_social_local += d_social_local
    st.session_state.cluster_broadly_socialized += d_broadly
    st.session_state.cluster_media_socialized += d_media
    st.session_state.cluster_low_pathway += d_low
    st.session_state.budget += profit
    
    st.session_state.history.append({
        "Saison": f"Jahr {st.session_state.saison}",
        "Ticketpreis (€)": price_ticket,
        "Equal-Pay Aufschlag (€)": equal_pay_surcharge,
        "Gesamtertrag (€)": rev_total,
        "Gewinn/Verlust (€)": profit,
        "Klub-Budget (€)": st.session_state.budget,
        "Gesamte Fanbase": (st.session_state.cluster_social_local + st.session_state.cluster_broadly_socialized + 
                            st.session_state.cluster_media_socialized + st.session_state.cluster_low_pathway)
    })
    
    if st.session_state.saison < st.session_state.max_saisons:
        st.session_state.saison += 1
    else:
        st.session_state.game_finished = True
        
    st.rerun()

# --- 6. BISHERIGE VERLAUFSTABELLE ---
if st.session_state.history:
    st.subheader("📋 Historie der Saisonergebnisse")
    st.table(pd.DataFrame(st.session_state.history))
