import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# --- Moderný dizajn a sticky horný panel ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon=":bar_chart:", layout="wide")

st.markdown("""
<style>
    .main-header {
        position: sticky;
        top: 0;
        z-index: 100;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        color: white;
        text-align: center;
        font-size: 1.3rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .sticky-summary {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 1rem 0.5rem 0.5rem 0.5rem;
        z-index: 9999;
        font-size: 1.2rem;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.08);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .variant-selector {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .note-cell {
        background: #fffbe6;
        border-radius: 5px;
        padding: 0.2rem 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar: variant, jednotky, filter fázy, reset ---
st.sidebar.header("Nastavenia")
variant = st.sidebar.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    help="Zvoľte typ soutěže."
)
unit_type = st.sidebar.radio(
    "Vyberte typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
    help="Vyberte, či chcete počítať len MP alebo aj transformačné plochy."
)

# --- Príprava dát ---
activities_data = ... # sem vložte pôvodné activities_data (nezmestí sa sem celý kvôli limitu)

df = pd.DataFrame(activities_data)
df["Poznámka"] = ""

# --- Filtrovanie podľa fázy ---
fazes = df["Fáze"].unique().tolist()
selected_fazes = st.sidebar.multiselect(
    "Filtrovať fázy:", fazes, default=fazes, help="Vyberte, ktoré fázy chcete zobraziť."
)

# --- Reset ---
if st.sidebar.button("Resetovať všetky hodnoty na default"):
    st.session_state.clear()
    st.experimental_rerun()

# --- Výber kľúčov podľa variantu a jednotiek ---
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"
jednotky_key = f"{ukey} jednotky - {vkey}"
cena_key = f"Cena za jednotku"

# --- Príprava editovateľnej tabuľky ---
df_filtered = df[df["Fáze"].isin(selected_fazes)].copy()
df_filtered["Množství"] = df_filtered[jednotky_key]
df_filtered["Cena za jednotku"] = df_filtered[cena_key]
df_filtered["Subtotal"] = df_filtered["Množství"] * df_filtered["Cena za jednotku"]

# --- Interaktívna tabuľka ---
edited_df = st.data_editor(
    df_filtered[["Fáze", "Aktivita", "Jednotka", "Množství", "Cena za jednotku", "Subtotal", "Poznámka"]],
    column_config={
        "Množství": st.column_config.NumberColumn("Množství", min_value=0, step=0.5, help="Zadajte počet jednotiek."),
        "Cena za jednotku": st.column_config.NumberColumn("Cena za jednotku", min_value=0, step=100, help="Zadajte cenu za jednotku."),
        "Poznámka": st.column_config.TextColumn("Poznámka", help="Vaša poznámka k aktivite.")
    },
    use_container_width=True,
    num_rows="dynamic",
    key="main_table"
)
edited_df["Subtotal"] = edited_df["Množství"] * edited_df["Cena za jednotku"]

# --- Rýchle sumáre ---
total = edited_df["Subtotal"].sum()
vat_amount = total * 0.21
total_with_vat = total * 1.21

# --- Sticky sumár dole ---
st.markdown(f"""
<div class="sticky-summary">
    <b>Celková suma bez DPH:</b> {total:,.0f} Kč &nbsp; | &nbsp;
    <b>DPH (21%):</b> {vat_amount:,.0f} Kč &nbsp; | &nbsp;
    <b>Celková suma s DPH:</b> {total_with_vat:,.0f} Kč
</div>
""", unsafe_allow_html=True)

# --- Grafy ---
st.markdown("---")
st.subheader("Vizualizace nákladů")
col1, col2 = st.columns(2)
with col1:
    fig_pie = px.pie(
        edited_df.groupby('Fáze')['Subtotal'].sum().reset_index(),
        values='Subtotal',
        names='Fáze',
        title='Rozložení nákladů podle fází',
        color_discrete_sequence=px.colors.sequential.Purples
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    fig_bar = px.bar(
        edited_df,
        x='Aktivita',
        y='Subtotal',
        color='Fáze',
        title='Náklady podle aktivit',
        color_discrete_sequence=px.colors.sequential.Purples
    )
    fig_bar.update_xaxes(tickangle=45)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Export ---
st.markdown("---")
st.subheader("Export výsledků")
col1, col2 = st.columns(2)
with col1:
    excel_buffer = BytesIO()
    edited_df.to_excel(excel_buffer, index=False)
    st.download_button(
        label="Stáhnout Excel",
        data=excel_buffer.getvalue(),
        file_name="soutezni_workshop_rozpocet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    st.info("Export do PDF bude čoskoro dostupný v ďalšej verzii.")

# --- Footer ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #666; padding: 2rem;'>Kalkulátor soutěžního workshopu | {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
