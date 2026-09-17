import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FanRadar Manager-Game", layout="wide")

# --- HEADER & MODUS-WAHL ---
st.title("⚽ FanRadar Manager-Game: Strategic Club Decision Engine")

mode = st.radio("🎮 Simulator-Modus wählen:", 
                ["Studierende (Geführte Szenarien & Lerneffekte)", 
                 "Vereins-Vorstand (Interaktives Multi-Year Management)"], 
                horizontal=True)

st.markdown("---")

# --- SIDEBAR: OPERATIVE ZAHNRÄDER (DECISIONS) ---
st.sidebar.header("🕹️ Operative Stellschrauben")

# Zahnrad 1: Akquise
st.sidebar.subheader("1. Akquise-Kanal & Budget")
acq_budget = st.sidebar.slider("Marketing-Budget (€)", 10000, 200000, 50000, step=10000)
acq_focus = st.sidebar.selectbox("Fokus des Kanals", 
                                ["Breitensport & Nachwuchs", "Performance & Social Media", "Equal Pay & Werte-Kommunikation"])

# Zahnrad 2: Pricing & Produkte
st.sidebar.subheader("2. Pricing & Stadion")
price_m = st.sidebar.slider("Ticketpreis Männer (€)", 15, 60, 30)
price_w = st.sidebar.slider("Ticketpreis Frauen (€)", 5, 30, 12)
merch_focus = st.sidebar.select_slider("Merchandising-Ausrichtung", options=["Basis (Klassisch)", "Balanced", "Nachhaltig & Premium"])

# Zahnrad 3: Haltung & Sponsoring
st.sidebar.subheader("3. Sponsoring & Haltung")
sponsor_type = st.sidebar.selectbox("Hauptsponsor-Kategorie", 
                                   ["Regionaler Mittelstand", "Global Player (Wettanbieter/Krypto)", "Nachhaltiges/Werte-Unternehmen"])
equal_pay_commitment = st.sidebar.slider("Equal Pay / Frauen-Investment (% vom Männer-Merch)", 0, 50, 10)

# --- ZAHNRAD-LOGIK & BERECHNUNGEN ---

# Baseline Fan-Verteilung
fans_tradition = 5000
fans_opportunist = 3000
fans_values = 2000

# WIRKUNG AKQUISE (Verschiebung der Cluster)
if acq_focus == "Breitensport & Nachwuchs":
    new_tradition = int(acq_budget / 10)
    new_opp = int(acq_budget / 20)
    new_val = int(acq_budget / 40)
elif acq_focus == "Performance & Social Media":
    new_tradition = int(acq_budget / 50)
    new_opp = int(acq_budget / 8)
    new_val = int(acq_budget / 25)
else: # Equal Pay & Werte
    new_tradition = int(acq_budget / 40)
    new_opp = int(acq_budget / 30)
    new_val = int(acq_budget / 7)

total_trad = fans_tradition + new_tradition
total_opp = fans_opportunist + new_opp
total_val = fans_values + new_val
total_fans = total_trad + total_opp + total_val

# WIRKUNG PRICING & EINSTELLUNGEN (Besuchs-Häufigkeit & WTP)
# Traditionsfans: Preissensibel bei Männern, neutral bei Frauen
visits_trad_m = np.clip(15 - (price_m - 25) * 0.3, 5, 17)
visits_trad_w = 2

# Opportunisten: Reagieren stark auf Leistung/Sponsor, nicht so preissensibel
visits_opp_m = np.clip(8 - (price_m - 35) * 0.1, 1, 15)
visits_opp_w = 3 if price_w <= 15 else 1

# Werte-Fans: Reagieren extrem positiv auf Equal Pay & Nachhaltigkeit, boykottieren Krypto/Wetten
val_multiplier = 1.5 if sponsor_type == "Nachhaltiges/Werte-Unternehmen" else (0.4 if sponsor_type == "Global Player (Wettanbieter/Krypto)" else 1.0)
visits_val_m = np.clip((6 + equal_pay_commitment * 0.1) * val_multiplier, 0, 17)
visits_val_w = np.clip((8 + equal_pay_commitment * 0.2) * val_multiplier, 0, 17)

# UMSATZ-BERECHNUNG
revenue_tickets_m = (total_trad * visits_trad_m + total_opp * visits_opp_m + total_val * visits_val_m) * price_m
revenue_tickets_w = (total_trad * visits_trad_w + total_opp * visits_opp_w + total_val * visits_val_w) * price_w

merch_spend_per_head = {"Basis (Klassisch)": 15, "Balanced": 25, "Nachhaltig & Premium": 40}[merch_focus]
revenue_merch = total_fans * merch_spend_per_head * (0.8 if sponsor_type == "Global Player (Wettanbieter/Krypto)" and acq_focus == "Equal Pay & Werte-Kommunikation" else 1.0)

sponsorship_base = {"Regionaler Mittelstand": 300000, "Global Player (Wettanbieter/Krypto)": 800000, "Nachhaltiges/Werte-Unternehmen": 500000}[sponsor_type]
total_revenue = revenue_tickets_m + revenue_tickets_w + revenue_merch + sponsorship_base

# RESILIENZ-INDEX (0 - 100%)
# Je ausgewogener das Portfolio und je höher die Loyalität, desto krisenfester
resilience_score = int(np.clip((total_trad * 0.5 + total_val * 0.4 + (100 - price_m) * 10) / (total_fans / 100), 20, 98))

# --- DASHBOARD ANZEIGE ---

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gesamt-Fans", f"{total_fans:,}".replace(",", "."))
col2.metric("Gesamtertrag (€)", f"{int(total_revenue):,}".replace(",", "."))
col3.metric("Ticket-Umsatz Frauen (€)", f"{int(revenue_tickets_w):,}".replace(",", "."))
col4.metric("Klub-Resilienz Index", f"{resilience_score} / 100")

st.markdown("---")

# DASHBOARD TABS
tab1, tab2, tab3 = st.tabs(["📊 Fan-Portfolio & Dynamik", "💰 Ertragsquellen", "🚨 Szenario- & Krisentest"])

with tab1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Entstandenes Fan-Portfolio")
        df_cluster = pd.DataFrame({
            "Fantyp": ["Traditions-Fans", "Opportunisten", "Werte-/Equal-Pay-Fans"],
            "Anzahl": [total_trad, total_opp, total_val]
        })
        fig_pie = px.pie(df_cluster, values="Anzahl", names="Fantyp", color="Fantyp",
                         color_discrete_map={"Traditions-Fans": "#1f77b4", "Opportunisten": "#ff7f0e", "Werte-/Equal-Pay-Fans": "#2ca02c"})
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_b:
        st.subheader("Stadionbesuche pro Jahr (Ø pro Kopf)")
        df_visits = pd.DataFrame({
            "Fantyp": ["Tradition", "Opportunist", "Werte-Fan"],
            "Männer-Spiele": [visits_trad_m, visits_opp_m, visits_val_m],
            "Frauen-Spiele": [visits_trad_w, visits_opp_w, visits_val_w]
        })
        fig_bar = px.bar(df_visits, x="Fantyp", y=["Männer-Spiele", "Frauen-Spiele"], barmode="group")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("Zusammensetzung der Einnahmen")
    df_rev = pd.DataFrame({
        "Quelle": ["Tickets Männer", "Tickets Frauen", "Merchandising", "Sponsoring"],
        "Betrag (€)": [revenue_tickets_m, revenue_tickets_w, revenue_merch, sponsorship_base]
    })
    fig_rev = px.bar(df_rev, x="Quelle", y="Betrag (€)", color="Quelle", text_auto='.2s')
    st.plotly_chart(fig_rev, use_container_width=True)

with tab3:
    st.subheader("Szenario-Simulation: Der Belastungstest")
    scenario = st.selectbox("Wähle ein Krisenszenario für die Saisonevaluierung:", 
                            ["Keine Krise (Normalbetrieb)", 
                             "Krise A: Hauptsponsor gerät in Imageskandal", 
                             "Krise B: Sportlicher Abstiegskampf Männer", 
                             "Krise C: Preiserhöhung löst Fan-Protest aus"])
    
    if scenario == "Krise A: Hauptsponsor gerät in Imageskandal":
        if sponsor_type == "Global Player (Wettanbieter/Krypto)":
            st.error("💥 **Schwere Auswirkung:** Die Werte-Fans boykottieren die Spiele komplett! Merch-Umsatz bricht um 40% ein.")
            st.metric("Neuer Gesamtertrag nach Krise", f"{int(total_revenue - revenue_merch * 0.4 - revenue_tickets_w * 0.5):,} €".replace(",", "."))
        else:
            st.success("✅ **Geringe Auswirkung:** Dank deines seriösen Sponsors bleibt der Reputationsschaden minimal.")
            
    elif scenario == "Krise B: Sportlicher Abstiegskampf Männer":
        st.warning("⚠️ **Gefahr:** Die Opportunisten bleiben im Männerstadion weg.")
        loss = (total_opp * visits_opp_m * 0.6) * price_m
        st.metric("Neuer Gesamtertrag nach Krise", f"{int(total_revenue - loss):,} €".replace(",", "."))
        st.info("💡 **Strategie-Tipp:** Klubs mit hohem Frauenfußball-Besuch und starken Werte-Fans kompensieren diesen Verlust deutlich besser.")

# WAS-WÄRE-WENN LERN-HINWEISE (Für Studierende)
if "Studierende" in mode:
    st.markdown("---")
    st.subheader("💡 Learning Insights")
    st.info(f"""
    * **Zahnrad Akquise & Fantyp:** Durch deinen Fokus auf **'{acq_focus}'** hast du primär den Typ **'{df_cluster.iloc[df_cluster['Anzahl'].idxmax()]['Fantyp']}'** aufgebaut.
    * **Equal Pay & Sponsoring Wechselwirkung:** Dein Equal-Pay Investment von **{equal_pay_commitment}%** harmoniert am besten mit einem werteorientierten Sponsor. 
    * **Resilienz:** Ein Resilienz-Score von **{resilience_score}/100** zeigt, wie stark deine Fanbase bei sportlichen oder wirtschaftlichen Krisen hinter dem Verein steht.
    """)
