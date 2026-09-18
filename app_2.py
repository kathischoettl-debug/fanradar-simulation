import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="FanRadar Strategic Engine", layout="wide")

# --- 1. INITIALISIERUNG DES KOMPLEXEN GAME-STATES ---
def init_game_state():
    default_values = {
        'saison': 1,
        'max_saisons': 4,
        'budget': 350000,
        # Die 4 empirischen Sozialisations-Cluster (Start-Verteilung)
        'cluster_social_local': 1065,
        'cluster_broadly_socialized': 882,
        'cluster_media_socialized': 885,
        'cluster_low_pathway': 747,
        # Formale Bindungsquoten (Startwerte)
        'dauerkarten_besitzer': 580,
        'vereinsmitglieder': 920,
        'history': [],
        'game_finished': False
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_game_state()

# --- 2. HEADER & SPIELENDE ---
st.title("⚽ FanRadar: Komplexe Vereins- & Markt-Simulation")

if st.session_state.game_finished:
    st.balloons()
    st.success("🎉 **4-Jahres-Planspiel abgeschlossen!** Detaillierte Bilanz deines Managements:")
    
    df_res = pd.DataFrame(st.session_state.history)
    st.dataframe(df_res, use_container_width=True)
    
    fig = px.line(df_res, x="Saison", y=["Gesamtertrag (€)", "Klub-Budget (€)", "Gesamte Fanbase", "Vereinsmitglieder"], markers=True, title="Entwicklung der Kernindikatoren über 4 Saisons")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔄 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_game_state()
        st.rerun()
    st.stop()

# Dashboard Top-KPIs
total_fans = (st.session_state.cluster_social_local + st.session_state.cluster_broadly_socialized + 
              st.session_state.cluster_media_socialized + st.session_state.cluster_low_pathway)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Aktuelle Runde", f"Saison {st.session_state.saison} / {st.session_state.max_saisons}")
m2.metric("Klub-Budget", f"{int(st.session_state.budget):,} €".replace(",", "."))
m3.metric("Gesamte Fanbase", f"{int(total_fans):,}".replace(",", "."))
m4.metric("Dauerkartenbesitzer", f"{int(st.session_state.dauerkarten_besitzer):,}".replace(",", "."))
m5.metric("Vereinsmitglieder", f"{int(st.session_state.vereinsmitglieder):,}".replace(",", "."))
m6.metric("Mitglieder-Quote", f"{round((st.session_state.vereinsmitglieder / total_fans)*100, 1)} %")

st.progress(st.session_state.saison / st.session_state.max_saisons)
st.markdown("---")

# --- 3. EXTERNE SZENARIEN & SZENARIO-KONTEXT ---
szenarien = {
    1: "📌 **Saison 1 - Touchpoint-Aufbau & Positionierung:** Setze das Grundfundament über Kanäle, Ticketpreise und Bindungsinstrumente.",
    2: "⚠️ **Saison 2 - Existenzielle Notlage (1860-Szenario):** Der Klub benötigt außerordentliche Hilfe zur Lizenzsicherung. Deine Bindungs-Cluster entscheiden über die Spendenbereitschaft!",
    3: "⚖️ **Saison 3 - Equal-Pay-Debatte & WTP-Test:** Die Haltung zu Equal Pay und Gender Equity Ethos wird von Fans und Medien kritisch reflektiert.",
    4: "⚡ **Saison 4 - Sponsoren-Ausrichtung:** Ein Großsponsor knüpft sein Angebot an die Kombination aus digitaler Reichweite und formaler Mitgliederbindung."
}

st.info(szenarien.get(st.session_state.saison, "Saison läuft..."))
st.subheader(f"⚙️ Umfassende Management-Stellschrauben (Saison {st.session_state.saison})")

# --- 4. VOLLER UMFANG: 12 DIFFERENZIERTE STELLSCHRAUBEN ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("**1. Touchpoint-Investition (Neukunden)**")
    inv_social_local = st.slider("Soziale & Lokale Wege (€)", 0, 50000, 15000, step=2500, help="Familie, Region, Stadionbesuche")
    inv_media = st.slider("Mediale Wege (€)", 0, 50000, 15000, step=2500, help="Online, Social Media, Live-Streams")
    inv_fankultur = st.slider("Organisierte Fankultur (€)", 0, 30000, 5000, step=2500, help="Fanclubs & Stammtische")

with c2:
    st.markdown("**2. Pricing & Ticket-Struktur**")
    price_tageskarte = st.slider("Tageskarte Männer (€)", 15, 60, 30)
    price_dauerkarte = st.slider("Dauerkarte Saison (€)", 200, 600, 350)
    equal_pay_surcharge = st.slider("Equal-Pay Aufschlag/Tageskarte (€)", 0, 10, 0, help="36,4% generelle Akzeptanz; höher bei SWO-Orientierung")

with c3:
    st.markdown("**3. Bindungs- & Community-Maßnahmen**")
    member_fee = st.slider("Mitgliedsbeitrag p.a. (€)", 40, 120, 60)
    member_perks = st.select_slider("Mitglieder-Vorteile & Stimmrecht", options=["Basis", "Erweitert", "Exklusiv & Community-Focus"])
    merch_sustainability = st.select_slider("Merch-Ausrichtung", options=["Standard Merch", "Nachhaltig & Premium"])

with c4:
    st.markdown("**4. Positionierung & Sponsoring**")
    swo_focus = st.selectbox(
        "Gender Equity & SWO-Ausrichtung",
        ["Neutrale Sport-Fokussierung", "Aktive SWO-Förderung (Support Women's Opportunity)"]
    )
    sponsoring_partner = st.selectbox(
        "Hauptsponsor-Profil",
        ["Regionaler Mittelstand (500k €)", "Wettanbieter / Krypto (900k €)", "Nachhaltigkeits-Brand (650k €)"]
    )
    profiling_depth = st.select_slider("Fan-Profiling & CRM-Tiefe", options=["Pragmatisch", "Standard", "Präzises CRM"])

st.markdown("---")

# --- 5. BERECHNUNGS-ENGINE (EMPIRISCH FUNDIERT) ---
if st.button(f"⏩ Saison {st.session_state.saison} simulieren", type="primary"):
    
    # Cost Accounting
    total_marketing_invest = inv_social_local + inv_media + inv_fankultur
    crm_cost = {"Pragmatisch": 5000, "Standard": 15000, "Präzises CRM": 35000}[profiling_depth]
    crm_efficiency = {"Pragmatisch": 0.85, "Standard": 1.0, "Präzises CRM": 1.25}[profiling_depth]
    
    # A. SOZIALISATIONS-NEUZUWÄCHSE
    d_social_local = int((inv_social_local / 12) * crm_efficiency)
    d_media = int((inv_media / 10) * crm_efficiency)
    d_broadly = int(((inv_social_local * 0.4 + inv_media * 0.4 + inv_fankultur * 0.5) / 15) * crm_efficiency)
    d_low = int((inv_media / 35))

    # B. FORMALE BINDUNG (DAUERKARTEN & MITGLIEDSCHAFTEN)
    # Empirisch: Broadly & Social-Local besitzen deutlich häufiger Dauerkarten & Mitgliedschaften
    dk_rate = (st.session_state.cluster_broadly_socialized * 0.211 +
               st.session_state.cluster_social_local * 0.194 +
               st.session_state.cluster_media_socialized * 0.049 +
               st.session_state.cluster_low_pathway * 0.066)
    
    member_rate = (st.session_state.cluster_broadly_socialized * 0.350 +
                  st.session_state.cluster_social_local * 0.285 +
                  st.session_state.cluster_media_socialized * 0.183 +
                  st.session_state.cluster_low_pathway * 0.180)
    
    # Preiselastizität auf Bindung
    dk_price_factor = max(0.6, 1.0 - (price_dauerkarte - 350) * 0.0015)
    member_price_factor = max(0.6, 1.0 - (member_fee - 60) * 0.003)
    
    new_dk = int(dk_rate * dk_price_factor)
    new_members = int(member_rate * member_price_factor)

    # C. STADIONBESUCHE & TICKET-REVENUE
    # Empirische Besuche/Jahr: Social-Local: 6.13 | Broadly: 6.65 | Media: 2.76 | Low-Pathway: 2.79
    price_penalty = max(0.5, 1.0 - (price_tageskarte - 30) * 0.012)
    
    vis_sl = 6.13 * price_penalty
    vis_br = 6.65 * price_penalty
    vis_med = 2.76 * price_penalty
    vis_low = 2.79 * price_penalty
    
    # Tageskartenkäufe (Gesamtbesuche abzüglich Abdeckung durch Dauerkarten)
    total_single_tickets = max(0, (
        st.session_state.cluster_social_local * vis_sl +
        st.session_state.cluster_broadly_socialized * vis_br +
        st.session_state.cluster_media_socialized * vis_med +
        st.session_state.cluster_low_pathway * vis_low
    ) - (new_dk * 17))
    
    # Equal-Pay Akzeptanz auf Tageskarten
    accept_rate = 0.364 if equal_pay_surcharge > 0 else 1.0
    if swo_focus == "Aktive SWO-Förderung (Support Women's Opportunity)":
        accept_rate += 0.18 # Booster durch aktivierte SWO-Motive
        
    effective_tageskarte_price = price_tageskarte + (equal_pay_surcharge * accept_rate)
    rev_tageskarten = total_single_tickets * effective_tageskarte_price
    rev_dauerkarten = new_dk * price_dauerkarte
    rev_mitglieder = new_members * member_fee

    # D. NOTHILFE-SZONARIO (SAISON 2)
    rev_nothilfe = 0
    if st.session_state.saison == 2:
        # Spendenbereitschaft: Broadly (76.2%), Social-Local (61.2%), Media (58.8%), Low (46.0%)
        # Mitglieder spenden mit 1.797-fach höheren Odds!
        member_booster = 1.3 if (new_members / total_fans) > 0.25 else 1.0
        rev_nothilfe = (
            (st.session_state.cluster_broadly_socialized * 0.762 * 60) +
            (st.session_state.cluster_social_local * 0.612 * 40) +
            (st.session_state.cluster_media_socialized * 0.588 * 20) +
            (st.session_state.cluster_low_pathway * 0.460 * 10)
        ) * member_booster
        st.toast(f"🚨 Nothilfe-Aktion erfolgreich: {int(rev_nothilfe):,} € wurden durch die Fanbase gespendet!")

    # E. MERCHANDISING & SPONSORING
    merch_spend = 40 if merch_sustainability == "Nachhaltig & Premium" else 22
    rev_merch = total_fans * merch_spend
    
    sponsor_base = {"Regionaler Mittelstand (500k €)": 500000, "Wettanbieter / Krypto (900k €)": 900000, "Nachhaltigkeits-Brand (650k €)": 650000}[sponsoring_partner]
    rev_sponsoring = sponsor_base

    # TOTALS
    rev_total = rev_tageskarten + rev_dauerkarten + rev_mitglieder + rev_merch + rev_sponsoring + rev_nothilfe
    exp_total = total_marketing_invest + crm_cost + 380000 # Betriebskosten
    profit = rev_total - exp_total
    
    # STATE UPDATE
    st.session_state.cluster_social_local += d_social_local
    st.session_state.cluster_broadly_socialized += d_broadly
    st.session_state.cluster_media_socialized += d_media
    st.session_state.cluster_low_pathway += d_low
    st.session_state.dauerkarten_besitzer = new_dk
    st.session_state.vereinsmitglieder = new_members
    st.session_state.budget += profit
    
    st.session_state.history.append({
        "Saison": f"Jahr {st.session_state.saison}",
        "Tageskarte M (€)": price_tageskarte,
        "Dauerkarte (€)": price_dauerkarte,
        "Equal-Pay Aufschlag (€)": equal_pay_surcharge,
        "Mitglieder": new_members,
        "Dauerkarten": new_dk,
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
