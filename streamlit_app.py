import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

# Nastavení stránky
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon=":cityscape:",
    layout="wide"
)

# Urbanistický styl a písmo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
    html, body {
        background: #f4f4f4;
        font-family: 'Montserrat', sans-serif;
    }
    .main-header {
        background: url('https://www.transparenttextures.com/patterns/asfalt-light.png'),
                    linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: #ecf0f1;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .subheader {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 0.5rem 0;
    }
    .phase-header {
        background: #27ae60;
        padding: 0.6rem;
        border-radius: 6px;
        color: white;
        margin-top: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: #ecf0f1;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .metric-card h3 {
        margin: 0;
        font-weight: 600;
    }
    .metric-card h2 {
        margin: 0.5rem 0 0;
        font-size: 1.5rem;
        font-weight: 800;
    }
    .footer {
        text-align: center;
        color: #95a5a6;
        padding: 2rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Základní data (předpokládá se df už načtené)
# Sidebar konfigurace
st.sidebar.header("Nastavení workshopu")
variant = st.sidebar.selectbox(
    "Variant workshopu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"]
)
unit_type = st.sidebar.selectbox(
    "Typ jednotek:",
    ["MP", "MP + TP"]
)
search_query = st.sidebar.text_input("🔍 Hledat aktivitu:")
selected_phases = st.sidebar.multiselect(
    "🗂️ Vyber fáze:",
    df["Fáze"].unique(), default=df["Fáze"].unique()
)

# Hlavní nadpis
st.markdown('<div class="main-header">Kalkulátor soutěžního workshopu</div>', unsafe_allow_html=True)

# Zpracování dat
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if unit_type == "MP" else "MP+TP"

df_filtered = df[df["Fáze"].isin(selected_phases)]
if search_query:
    df_filtered = df_filtered[df_filtered["Aktivita"].str.contains(search_query, case=False, na=False)]

selected_activities, total, selected_count = [], 0, 0

# Výpis fází a aktivit
for faze in selected_phases:
    fase_df = df_filtered[df_filtered["Fáze"] == faze]
    if fase_df.empty:
        continue
    st.markdown(f'<div class="phase-header">🏙️ {faze}</div>', unsafe_allow_html=True)
    faze_total = 0
    for idx, row in fase_df.iterrows():
        with st.expander(f"{row['Aktivita']}"):
            default_units = row.get(f"{ukey} jednotky - {vkey}", 0) or 0
            units = st.number_input(
                "Množství:", value=float(default_units), step=0.5,
                key=f"u_{faze}_{idx}"
            )
            subtotal = units * row['Cena za jednotku']
            cols = st.columns(3)
            cols[0].markdown(f"**Jednotka:** {row['Jednotka']}")
            cols[1].markdown(f"**Cena/jedn.:** {row['Cena za jednotku']:,} Kč")
            cols[2].markdown(f"**Subtotal:** {subtotal:,} Kč")
            if units > 0:
                selected_activities.append({
                    'Fáze': faze, 'Aktivita': row['Aktivita'],
                    'Množství': units, 'Cena': subtotal
                })
                faze_total += subtotal
                total += subtotal
                selected_count += 1
    if faze_total:
        st.markdown(f'<div class="metric-card">Celkem {faze}:<br><strong>{faze_total:,} Kč</strong></div>', unsafe_allow_html=True)

# Stavový pruh
st.progress(selected_count / len(df) if df.shape[0] else 0)

# Vizualizace nákladů
if selected_activities:
    st.markdown('<div class="subheader">Vizualizace nákladů podle fází a aktivit</div>', unsafe_allow_html=True)
    df_sel = pd.DataFrame(selected_activities)
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.pie(
            df_sel.groupby('Fáze')['Cena'].sum().reset_index(),
            names='Fáze', values='Cena', hole=0.4,
            title='Podíl nákladů dle fází'
        )
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.bar(
            df_sel, x='Aktivita', y='Cena', color='Fáze',
            title='Náklady dle aktivit'
        )
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)

# Shrnutí a export
st.markdown('<hr>', unsafe_allow_html=True)
vat = total * 0.21
 tot_vat = total + vat
st.markdown('<div class="metric-grid">', unsafe_allow_html=True)('<div class="metric-grid">', unsafe_allow_html=True)
for title, amount in [('Bez DPH', total), ('DPH 21%', vat), ('Celkem s DPH', tot_vat)]:
    st.markdown(f'<div class="metric-card"><h3>{title}</h3><h2>{amount:,} Kč</h2></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer with corrected f-string syntax
st.markdown(f"<div class=\"footer\">Aktualizováno: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
