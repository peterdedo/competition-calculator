import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page Configuration and Styling ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon=":cityscape:", layout="wide")
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
    body { background: #f4f4f4; font-family: 'Montserrat', sans-serif; }
    .main-header { background: linear-gradient(135deg, #2c3e50, #34495e); padding: 1.5rem; border-radius: 12px;
                    color: #ecf0f1; text-align: center; font-size: 2.2rem; font-weight: 800;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.2); margin-bottom: 2rem; }
    .phase-header { background: #27ae60; padding: 0.8rem; border-radius: 6px; color: white;
                    margin-top: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; }
    .metric-card { background: #ecf0f1; padding: 1rem; border-radius: 10px;
                    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    color: #2c3e50; margin-bottom: 1rem; }
    .subheader { color: #2c3e50; font-size: 1.4rem; font-weight: 600; margin-top: 2.5rem; }
    .metric-grid { display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:1rem; margin:2rem 0; }
    .footer { text-align: center; color: #95a5a6;
               padding: 2rem 0; font-size:0.9rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_activities():
    activities = [
        # Zde je kompletní seznam všech aktivit (včetně cenových jednotek apod.)
        {"Fáze":"Analytická fáze","Aktivita":"Sestavení řídící skupiny","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":1.0,"MP jednotky - CZ":1.0,"MP+TP jednotky - MEZ":2.0,"MP+TP jednotky - CZ":2.0},
        {"Fáze":"Analytická fáze","Aktivita":"Vymezení řešeného území","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":1.0,"MP jednotky - CZ":1.0,"MP+TP jednotky - MEZ":2.0,"MP+TP jednotky - CZ":2.0},
        {"Fáze":"Analytická fáze","Aktivita":"Seznámení se s dostupnými materiály a záměry v území","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":6.0,"MP jednotky - CZ":6.0,"MP+TP jednotky - MEZ":8.0,"MP+TP jednotky - CZ":8.0},
        {"Fáze":"Analytická fáze","Aktivita":"Analýza stavu území na základě předem definovaných parametrů a indikátorů","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":32.0,"MP jednotky - CZ":32.0,"MP+TP jednotky - MEZ":42.0,"MP+TP jednotky - CZ":42.0},
        {"Fáze":"Analytická fáze","Aktivita":"Kompletace výstupu z analýzy jako podkladu pro zadání soutěže","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":8.0,"MP jednotky - CZ":8.0,"MP+TP jednotky - MEZ":11.0,"MP+TP jednotky - CZ":11.0},
        {"Fáze":"Analytická fáze","Aktivita":"Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":3.0,"MP jednotky - CZ":3.0,"MP+TP jednotky - MEZ":6.0,"MP+TP jednotky - CZ":6.0},
        # ... (doplňte všechny zbývající fáze a aktivity stejným formátem) ...
    ]
    return pd.DataFrame(activities)

df = load_activities()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Nastavení workshopu")
    variant = st.selectbox("Variant workshopu:", ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"])
    unit_type = st.selectbox("Typ jednotek:", ["MP", "MP + TP"])
    search_query = st.text_input("🔍 Hledat aktivitu:")
    phases = st.multiselect("🗂️ Vyber fáze:", df["Fáze"].unique(), default=df["Fáze"].unique())

# --- Main Header ---
st.markdown('<div class="main-header">Kalkulátor soutěžního workshopu</div>', unsafe_allow_html=True)

# --- Data Preparation ---
df_filtered = df[df["Fáze"].isin(phases)]
if search_query:
    df_filtered = df_filtered[df_filtered["Aktivita"].str.contains(search_query, case=False, na=False)]
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = unit_type.replace(" ", "")
unit_col = f"{ukey} jednotky - {vkey}"

# --- Activity Selection & Calculation ---
selected = []
total_cost = 0
count = 0
for phase in phases:
    phase_df = df_filtered[df_filtered["Fáze"] == phase]
    if phase_df.empty:
        continue
    st.markdown(f'<div class="phase-header">🏙️ {phase}</div>', unsafe_allow_html=True)
    phase_sum = 0
    for idx, row in phase_df.iterrows():
        with st.expander(row['Aktivita']):
            default_qty = row.get(unit_col, 0) or 0
            qty = st.number_input("Množství:", min_value=0.0, value=float(default_qty), step=0.5, key=f"qty_{phase}_{idx}")
            cost = qty * row['Cena za jednotku']
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Jednotka:** {row['Jednotka']}")
            c2.markdown(f"**Cena/jednotku:** {row['Cena za jednotku']:,} Kč")
            c3.markdown(f"**Subtotal:** {cost:,} Kč")
            if qty > 0:
                selected.append({'Fáze': phase, 'Aktivita': row['Aktivita'], 'Množství': qty, 'Cena': cost})
                phase_sum += cost
                total_cost += cost
                count += 1
    if phase_sum > 0:
        st.markdown(f'<div class="metric-card">Celkem {phase}:<br><strong>{phase_sum:,} Kč</strong></div>', unsafe_allow_html=True)

# --- Progress Indicator ---
st.progress(min(count / len(df), 1.0))

# --- Visualization ---
if selected:
    st.markdown('<div class="subheader">Vizualizace nákladů</div>', unsafe_allow_html=True)
    sel_df = pd.DataFrame(selected)
    left, right = st.columns(2)
    left.plotly_chart(
        px.pie(sel_df.groupby('Fáze')['Cena'].sum().reset_index(), names='Fáze', values='Cena', hole=0.4),
        use_container_width=True
    )
    right.plotly_chart(
        px.bar(sel_df, x='Aktivita', y='Cena', color='Fáze').update_layout(xaxis_tickangle=45),
        use_container_width=True
    )

# --- Summary and Footer ---
vat = total_cost * 0.21
with_vat = total_cost + vat
st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
for title, val in [('Bez DPH', total_cost), ('DPH 21%', vat), ('Celkem s DPH', with_vat)]:
    st.markdown(f'<div class="metric-card"><h3>{title}</h3><h2>{val:,} Kč</h2></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<div class='footer'>Aktualizováno: {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
