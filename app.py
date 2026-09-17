import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="FanRadar Simulation", layout="wide")

st.title("⚽ FanRadar Decision Engine")
st.markdown("Simulationsmodell zur Wirkung von Preis- & Equal-Pay-Initiativen im Männer- und Frauenfußball.")

# --- SIDEBAR: MODUS & EINSTELLUNGEN ---
st.sidebar.header("🎯 Simulations-Modus")
mode = st.sidebar.radio("Wähle deine Zielgruppe:", ["Studierende (Didaktisch)", "Vereine (Strategisch/Stochastisch)"])

st.sidebar.markdown("---")
st.sidebar.header("🕹️ Stellschrauben (Inputs)")

# Inputs
price_increase = st.sidebar.slider("Preisanpassung Damen-Tickets (%)", 0, 100, 20)
swo_budget = st.sidebar.slider("SWO / Aktivierungsbudget (€)", 0, 100000, 25000, step=5000)
framing = st.sidebar.selectbox("Kommunikations-Framing", ["Reinvestition Nachwuchs", "Allgemeine Preisanpassung", "Equal Pay Initiative"])

# --- MATHEMATISCHE SIMULATIONS-LOGIK ---
framing_bonus = {"Reinvestition Nachwuchs": 1.2, "Equal Pay Initiative": 1.1, "Allgemeine Preisanpassung": 0.8}[framing]

# WTP-Wahrscheinlichkeit & Mittlere WTP
base_wtp_prob = 0.364
wtp_probability = np.clip(base_wtp_prob + (swo_budget / 200000) * 0.15 * framing_bonus - (price_increase / 100) * 0.1, 0, 1)

base_wtp_eur = 12.50
estimated_wtp_eur = base_wtp_eur * (1 + (swo_budget / 100000) * 0.25 * framing_bonus) * (1 - (price_increase / 100) * 0.05)

# --- DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns(3)
col1.metric("WTP-Wahrscheinlichkeit (Fanbase)", f"{wtp_probability * 100:.1f}%")
col2.metric("Geschätzte Ø Zahlungsbereitschaft", f"{estimated_wtp_eur:.2f} €")
col3.metric("Erwarteter Zusatzumsatz", f"{int(swo_budget * 1.4 * framing_bonus):,} €".replace(",", "."))

st.markdown("---")

# --- MODUS-SPEZIFISCHER CONTENT ---
if mode == "Studierende (Didaktisch)":
    st.subheader("📚 Didaktische Analyse: Ursache-Wirkungskette")
    
    st.info(f"""
    **Lern-Hinweis:** Das gewählte Framing **"{framing}"** verändert die Akzeptanz der Preiserhöhung. 
    Höhere Aktivierungsbudgets stärken das SWO-Motiv (*Support Women's Opportunity*), was den negativen Preiselastizitätseffekt dämpft.
    """)
    
    # Sensitivitäts-Chart
    budget_range = np.linspace(0, 100000, 20)
    wtp_curve = [base_wtp_eur * (1 + (b / 100000) * 0.25 * framing_bonus) for b in budget_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=budget_range, y=wtp_curve, mode='lines+markers', name='Ø WTP (€)'))
    fig.update_layout(title="Sensitivität: Budget vs. Zahlungsbereitschaft", xaxis_title="Budget (€)", yaxis_title="WTP (€)")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.subheader("📊 Vereins-Dashboard: Stochastische Risikobewertung (Monte-Carlo)")
    
    # Monte-Carlo Simulation
    np.random.seed(42)
    simulations = np.random.normal(loc=estimated_wtp_eur, scale=estimated_wtp_eur * 0.15, size=2000)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=simulations, nbinsx=30, name='WTP-Verteilung', marker_color='#1f77b4'))
    fig.update_layout(title="Monte-Carlo-Verteilung der WTP unter Unsicherheit (N=2.000)", xaxis_title="Zahlungsbereitschaft (€)", yaxis_title="Häufigkeit")
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("⚠️ **Risiko-Hinweis für den Vorstand:** Bei aktuellem Setup liegt das 95%-Konfidenzintervall der Erträge zwischen "
               f"{np.percentile(simulations, 2.5):.2f} € und {np.percentile(simulations, 97.5):.2f} € pro Ticket.")
