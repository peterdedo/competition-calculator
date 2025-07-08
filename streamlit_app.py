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

# Moderný dizajn
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon=":bar_chart:",
    layout="wide"
)

# Vlastní styl
st.markdown("""
<style>
    .main-header { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 8px; color: white; text-align: center; font-size: 1.3rem; margin-bottom: 1rem; }
    .phase-header { background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%); padding: 0.5rem; border-radius: 6px; color: white; margin-top: 1rem; font-weight: 600; }
    .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; color: white; text-align: center; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Sidebar: nastavení varianty, typ, filtry
st.sidebar.header("Nastavení");
variant = st.sidebar.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"]
)
unit_type = st.sidebar.radio(
    "Typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"]
)

# Načtení dat
activities_data = [
    # (data jako dříve...)
]
df = pd.DataFrame(activities_data)
fazes = list(df["Fáze"].unique())

# Filtry
search_query = st.sidebar.text_input("Hledat aktivitu:")
selected_phases = st.sidebar.multiselect("Vyber fáze:", fazes, default=fazes)

# Výpočet klíčů
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# Hlavní nadpis
st.markdown(f"<div class='main-header'><h1>Kalkulátor soutěžního workshopu</h1></div>", unsafe_allow_html=True)

# Iterace přes fáze
selected_activities = []
total = 0
selected_count = 0
for faze in faze_df_unique := fazes:
    if faze not in selected_phases:
        continue
    faze_df = df[df["Fáze"] == faze]
    if search_query:
        faze_df = faze_df[faze_df["Aktivita"].str.contains(search_query, case=False, na=False)]
        if faze_df.empty:
            continue
    st.markdown(f"<div class='phase-header'>{faze}</div>", unsafe_allow_html=True)
    faze_total = 0

    for i, row in faze_df.iterrows():
        key = f"units_{faze}_{i}"
        default_units = row.get(f"{ukey} jednotky - {vkey}", 0)
        max_units = float(row.get("Cena za jednotku", 0))
        with st.expander(row["Aktivita"]):
            units = st.number_input(
                "Jednotek:", min_value=0.0, value=float(default_units), step=0.5, key=key
            )
            subtotal = units * row["Cena za jednotku"]
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Jednotka:** {row['Jednotka']}")
                st.write(f"**Cena za jednotku:** {row['Cena za jednotku']:,} Kč")
            with col2:
                st.write(f"**Subtotal:** {subtotal:,} Kč")
                st.write(f"**Původní cena:** {row.get(f'Cena {ukey} - {vkey}', 0):,} Kč")
            if units > 0:
                selected_activities.append({
                    "Fáze": faze,
                    "Aktivita": row['Aktivita'],
                    "Jednotka": row['Jednotka'],
                    "Množství": units,
                    "Cena za jednotku": row['Cena za jednotku'],
                    "Subtotal": subtotal
                })
                faze_total += subtotal
                total += subtotal
                selected_count += 1

    if faze_total > 0:
        st.markdown(f"<div class='metric-card'><strong>{faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)

# Pokrok
progress = selected_count / len(df) if df.shape[0] else 0
st.progress(progress, text=f"Vybráno: {selected_count}/{df.shape[0]}")

# Vizualizace
if selected_activities:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='main-header'><h2>Vizualizace</h2></div>", unsafe_allow_html=True)
    df_sel = pd.DataFrame(selected_activities)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df_sel.groupby('Fáze')['Subtotal'].sum().reset_index(), values='Subtotal', names='Fáze', title='Náklady podle fází')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(df_sel, x='Aktivita', y='Subtotal', color='Fáze', title='Náklady podle aktivit')
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)

# Výsledky
st.markdown("<hr>", unsafe_allow_html=True)
vat = total * 0.21
tot_vat = total + vat
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-card'><h3>Bez DPH</h3><h2>{total:,} Kč</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><h3>DPH (21%)</h3><h2>{vat:,} Kč</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><h3>S DPH</h3><h2>{tot_vat:,} Kč</h2></div>", unsafe_allow_html=True)

# Detail a export jako dříve...
st.markdown(f"<div style='text-align:center; color:#888; padding:1rem;'>Aktualizováno: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
