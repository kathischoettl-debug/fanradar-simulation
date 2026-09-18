# ÄNDERUNG IN COL1 (Zeile 66):
acq_focus = st.selectbox(
    "Akquise-Kanal / Zielgruppe", 
    [
        "Breitensport & Nachwuchs (Fokus: Cluster 1 - Kernfans)", 
        "Performance & Social Media (Fokus: Cluster 2 - Event-Fans)", 
        "Equal Pay & Werte-Kommunikation (Fokus: Cluster 3 - Equal-Pay-Fans)"
    ]
)

# ÄNDERUNG IN DER BERECHNUNGS-LOGIK (Zeile 88):
if "Breitensport" in acq_focus:
    d_kern = int((acq_budget / 8) * seg_efficiency)
    d_event = int(acq_budget / 20)
    d_equal = int(acq_budget / 30)
elif "Performance" in acq_focus:
    d_kern = int(acq_budget / 40)
    d_event = int((acq_budget / 6) * seg_efficiency * hype)
    d_equal = int(acq_budget / 20)
else: # Equal Pay
    d_kern = int(acq_budget / 30)
    d_event = int(acq_budget / 25)
    d_equal = int((acq_budget / 5) * seg_efficiency * hype)
