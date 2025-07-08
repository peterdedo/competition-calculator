import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Constants & Styling ---
PAGE_TITLE = "Kalkulátor soutěžního workshopu"
PAGE_ICON = ":cityscape:"
FONT_FAMILY = "'Montserrat', sans-serif"
BG_COLOR = "#f4f4f4"
HEADER_GRADIENT = "linear-gradient(135deg, #2c3e50, #34495e)"
PHASE_COLOR = "#27ae60"
CARD_BG = "#ecf0f1"
CARD_SHADOW = "0 2px 8px rgba(0,0,0,0.1)"

# CSS injection
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
    body {{ background: {BG_COLOR}; font-family: {FONT_FAMILY}; }}
    .main-header {{ background: {HEADER_GRADIENT}; padding: 1.2rem; border-radius: 10px;
                     color: #ecf0f1; text-align: center; font-size: 2rem; font-weight: 800;
                     box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 1.5rem; }}
    .phase-header {{ background: {PHASE_COLOR}; padding: 0.6rem; border-radius: 6px; color: white;
                     margin-top: 1rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
    .metric-card {{ background: {CARD_BG}; padding: 1rem; border-radius: 8px;
                     text-align: center; box-shadow: {CARD_SHADOW};
                     color: #2c3e50; margin-bottom: 1rem; }}
    .subheader {{ color: #2c3e50; font-size: 1.3rem; font-weight: 600; margin-top: 2rem; }}
    .metric-grid {{ display: grid;
                     grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap:1rem; margin:1.5rem 0; }}
    .footer {{ text-align: center; color: #95a5a6;
               padding: 2rem 0; font-size:0.9rem; }}
</style>
""", unsafe_allow_html=True)

# --- Data Loading with Caching ---
@st.cache_data
def load_activities():
    # Ideally load from external CSV/JSON
    # For demo purposes, inline a subset
    data = [
        {"Fáze": "Analytická fáze", "Aktivita": "Sestavení řídící skupiny", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MEZ_MP": 1.0, "CZ_MP": 1.0, "MEZ_MP+TP": 2.0, "CZ_MP+TP": 2.0},
        # ... add the rest of activities here with consistent keys ...
    ]
    df = pd.DataFrame(data)
    # Rename columns for dynamic access
    df.columns = df.columns.str.replace("MP jednotky - ", "").str.replace("Cena za jednotku", "Cena/jednotku")
    return df

df = load_activities()
if df.empty:
    st.error("Data aktivit nejsou k dispozici.")
    st.stop()

# --- Sidebar Controls ---
st.sidebar.header("Nastavení workshopu")
variant = st.sidebar.selectbox("Variant workshopu:", ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"])
unit_type = st.sidebar.selectbox("Typ jednotek:", ["MP", "MP + TP"])
search_query = st.sidebar.text_input("🔍 Hledat aktivitu:")
selected_phases = st.sidebar.multiselect(
    "🗂️ Vyber fáze:", df["Fáze"].unique(), default=df["Fáze"].unique()
)

# --- Header ---
st.markdown(f'<div class="main-header">{PAGE_TITLE}</div>', unsafe_allow_html=True)

# --- Key Calculation ---
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = unit_type.replace(" "+"+TP", "+TP")

# --- Filter Data ---
filtered = df[df["Fáze"].isin(selected_phases)]
if search_query:
    filtered = filtered[filtered["Aktivita"].str.contains(search_query, case=False, na=False)]

selected_items = []
total_cost = 0

# --- Activity Selection and Calculation ---
for phase in selected_phases:
    phase_df = filtered[filtered["Fáze"] == phase]
    if phase_df.empty:
        continue
    st.markdown(f'<div class="phase-header">🏙️ {phase}</div>', unsafe_allow_html=True)
    phase_cost = 0
    for idx, row in phase_df.iterrows():
        default_qty = row.get(f"{vkey}_{ukey}", 0)
        qty = st.number_input(
            f"{row['Aktivita']} - Množství:", min_value=0.0, value=float(default_qty), step=0.5, key=f"qty_{idx}"
        )
        cost = qty * row['Cena/jednotku']
        cols = st.columns(3)
        cols[0].markdown(f"**Jednotka:** {row['Jednotka']}")
        cols[1].markdown(f"**Cena/jednotku:** {row['Cena/jednotku']:,} Kč")
        cols[2].markdown(f"**Subtotal:** {cost:,} Kč")
        if qty:
            selected_items.append({'Fáze': phase, 'Aktivita': row['Aktivita'], 'Množství': qty, 'Cena': cost})
            phase_cost += cost
            total_cost += cost
    if phase_cost:
        st.markdown(f'<div class="metric-card">Celkem {phase}:<br><strong>{phase_cost:,} Kč</strong></div>', unsafe_allow_html=True)

# --- Progress Indicator ---
st.progress(min(len(selected_items)/len(df), 1.0))

# --- Visualization ---
if selected_items:
    st.markdown('<div class="subheader">Vizualizace nákladů</div>', unsafe_allow_html=True)
    sel_df = pd.DataFrame(selected_items)
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.pie(sel_df.groupby('Fáze')['Cena'].sum().reset_index(), names='Fáze', values='Cena', hole=0.4),
        use_container_width=True
    )
    c2.plotly_chart(
        px.bar(sel_df, x='Aktivita', y='Cena', color='Fáze').update_layout(xaxis_tickangle=45),
        use_container_width=True
    )

# --- Summary & Metrics ---
vat = total_cost * 0.21
total_with_vat = total_cost + vat
st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
for title, amt in [('Bez DPH', total_cost), ('DPH 21%', vat), ('Celkem s DPH', total_with_vat)]:
    st.markdown(f'<div class="metric-card"><h3>{title}</h3><h2>{amt:,} Kč</h2></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"<div class=\"footer\">Aktualizováno: {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
