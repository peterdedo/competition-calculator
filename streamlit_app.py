import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon="📊",
    layout="wide"
)

# --- Custom Styles ---
st.markdown("""
<style>
  .header {background: linear-gradient(90deg,#667eea,#764ba2);padding:1rem;border-radius:0.5rem;color:#fff;text-align:center;}
  .subheader {font-size:1.2rem;margin-top:1rem;font-weight:600;color:#333;}
  .metric-card {background: linear-gradient(135deg,#667eea,#764ba2);padding:1rem;border-radius:1rem;color:#fff;text-align:center;}
  .sidebar .stNumberInput label {font-weight:500;}
  .btn-download {margin-top:0.5rem;}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Parametry kalkulace")
variant = st.sidebar.selectbox(
    "Varianta soutěže:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"]
)
unit_type = st.sidebar.selectbox(
    "Typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"]
)
search_term = st.sidebar.text_input("🔍 Hledat aktivitu")

# --- Data Definition ---
@st.experimental_memo
def load_data():
    return pd.DataFrame([
        # Vložen kompletní seznam aktivit
        {"Fáze":"Analytická fáze","Aktivita":"Sestavení řídící skupiny","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":1.0,"MP jednotky - CZ":1.0,"MP+TP jednotky - MEZ":2.0,"MP+TP jednotky - CZ":2.0},
        {"Fáze":"Analytická fáze","Aktivita":"Vymezení řešeného území","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":1.0,"MP jednotky - CZ":1.0,"MP+TP jednotky - MEZ":2.0,"MP+TP jednotky - CZ":2.0},
        {"Fáze":"Analytická fáze","Aktivita":"Seznámení se s dostupnými materiály a záměry v území","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":6.0,"MP jednotky - CZ":6.0,"MP+TP jednotky - MEZ":8.0,"MP+TP jednotky - CZ":8.0},
        {"Fáze":"Analytická fáze","Aktivita":"Analýza stavu území na základě předem definovaných parametrů a indikátorů","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":32.0,"MP jednotky - CZ":32.0,"MP+TP jednotky - MEZ":42.0,"MP+TP jednotky - CZ":42.0},
        {"Fáze":"Analytická fáze","Aktivita":"Kompletace výstupu z analýzy jako podkladu pro zadání soutěže","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":8.0,"MP jednotky - CZ":8.0,"MP+TP jednotky - MEZ":11.0,"MP+TP jednotky - CZ":11.0},
        {"Fáze":"Analytická fáze","Aktivita":"Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":3.0,"MP jednotky - CZ":3.0,"MP+TP jednotky - MEZ":6.0,"MP+TP jednotky - CZ":6.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":15.0,"MP jednotky - CZ":15.0,"MP+TP jednotky - MEZ":20.0,"MP+TP jednotky - CZ":20.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Sestavení podrobného rozpočtu","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":3.0,"MP jednotky - CZ":2.0,"MP+TP jednotky - MEZ":4.0,"MP+TP jednotky - CZ":3.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":10.0,"MP jednotky - CZ":10.0,"MP+TP jednotky - MEZ":15.0,"MP+TP jednotky - CZ":15.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":0.0,"MP jednotky - CZ":0.0,"MP+TP jednotky - MEZ":15.0,"MP+TP jednotky - CZ":15.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Vytvoření značky soutěže (včetně konzultace se zadavatelem)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":4.0,"MP jednotky - CZ":4.0,"MP+TP jednotky - MEZ":4.0,"MP+TP jednotky - CZ":4.0},
        {"Fáze":"Přípravní fáze","Aktivita":"PR strategie projektu","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":4.0,"MP jednotky - CZ":3.0,"MP+TP jednotky - MEZ":4.0,"MP+TP jednotky - CZ":3.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Kompletace zadání (parametry využití území, stavební program, průběžná jednání s ŘS a PS)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":30.0,"MP jednotky - CZ":25.0,"MP+TP jednotky - MEZ":50.0,"MP+TP jednotky - CZ":40.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Formulace soutěžních podmínek","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":16.0,"MP jednotky - CZ":16.0,"MP+TP jednotky - MEZ":20.0,"MP+TP jednotky - CZ":20.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Finalizace a publikace soutěžních podmínek a zadání","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":4.0,"MP jednotky - CZ":4.0,"MP+TP jednotky - MEZ":5.0,"MP+TP jednotky - CZ":5.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Sestavení poroty","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":6.0,"MP jednotky - CZ":5.0,"MP+TP jednotky - MEZ":9.0,"MP+TP jednotky - CZ":8.0},
        {"Fáze":"Přípravní fáze","Aktivita":"Kompletace před vyhlášením soutěže a ustavující schůze poroty (včetně regulérnosti ČKA)","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":23.0,"MP jednotky - CZ":23.0,"MP+TP jednotky - MEZ":25.0,"MP+TP jednotky - CZ":25.0},
        {"Fáze":"Průběh soutěžního workshopu (SW)","Aktivita":"Vyhlášení soutěže – otevřená výzva a výběr soutěžících","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":7.0,"MP jednotky - CZ":5.0,"MP+TP jednotky - MEZ":7.0,"MP+TP jednotky - CZ":5.0},
        {"Fáze":"Průběh soutěžního workshopu (SW)","Aktivita":"Příprava a organizace 1. SW","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":30.0,"MP jednotky - CZ":25.0,"MP+TP jednotky - MEZ":30.0,"MP+TP jednotky - CZ":25.0},
        {"Fáze":"Průběh soutěžního workshopu (SW)","Aktivita":"Příprava a organizace 2. SW","Jednotka":"den","Cena za jednotku":14000.0,"MP jednotky - MEZ":30.0,"MP jednotky - CZ":25.0,"
    ])

df = load_data()
vkey = "MEZ" if variant.startswith("Mezinárodní") else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# Filter by search
df = df[df['Aktivita'].str.contains(search_term, case=False, na=False)] if search_term else df

# --- Main Header ---
st.markdown(f"<div class='header'><h1>Kalkulátor soutěžního workshopu</h1><p>Varianta: {variant} | Jednotky: {unit_type}</p></div>", unsafe_allow_html=True)

# --- Tabs: Výběr, Vizualizace, Export ---
tab1, tab2, tab3 = st.tabs(["Výběr aktivit", "Vizualizace", "Export"])
selected = []

with tab1:
    st.markdown("<div class='subheader'>Výběr aktivit</div>", unsafe_allow_html=True)
    for faze in df['Fáze'].unique():
        st.markdown(f"<h3>{faze}</h3>", unsafe_allow_html=True)
        faze_df = df[df['Fáze']==faze]
        for idx, row in faze_df.iterrows():
            cols = st.columns([3,1])
            with cols[0]:
                units = st.number_input(
                    f"{row['Aktivita']}",
                    min_value=0.0,
                    value=float(row.get(f"{ukey} jednotky - {vkey}",0)),
                    step=0.5,
                    key=f"u_{idx}"
                )
            subtotal = units * row['Cena za jednotku']
            cols[1].markdown(f"**{subtotal:,.0f} Kč**")
            if units>0:
                selected.append({
                    'Fáze':row['Fáze'],'Aktivita':row['Aktivita'],'Jednotka':row['Jednotka'],
                    'Množství':units,'Cena za jednotku':row['Cena za jednotku'],'Subtotal':subtotal
                })

with tab2:
    st.markdown("<div class='subheader'>Vizualizace nákladů</div>", unsafe_allow_html=True)
    if selected:
        sel_df = pd.DataFrame(selected)
        pie = px.pie(sel_df.groupby('Fáze')['Subtotal'].sum().reset_index(), names='Fáze', values='Subtotal', title='Rozložení podle fází')
        bar = px.bar(sel_df, x='Aktivita', y='Subtotal', color='Fáze', title='Náklady dle aktivity')
        bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(pie, use_container_width=True)
        st.plotly_chart(bar, use_container_width=True)
    else:
        st.info("Vyberte alespoň jednu aktivitu v záložce 'Výběr aktivit'.")

with tab3:
    st.markdown("<div class='subheader'>Souhrn a export</div>", unsafe_allow_html=True)
    if selected:
        sel_df = pd.DataFrame(selected)
        total = sel_df['Subtotal'].sum()
        vat = total*0.21
        total_vat = total+vat
        c1,c2,c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h4>Bez DPH</h4><h2>{total:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h4>DPH 21%</h4><h2>{vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h4>S DPH</h4><h2>{total_vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        st.dataframe(sel_df, use_container_width=True)
        csv = sel_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv, file_name="rozpocet.csv", mime='text/csv', css_class='btn-download')
        # PDF
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4)
        elems=[Paragraph("Report", getSampleStyleSheet()['Heading1']), Spacer(1,12)]
        data=[['Fáze','Aktivita','Jednotka','Množství','Cena','Subtotal']]
        for _,r in sel_df.iterrows(): data.append([r['Fáze'],r['Aktivita'],r['Jednotka'],r['Množství'],f"{r['Cena za jednotku']:,.0f}",f"{r['Subtotal']:,.0f}"])
        tbl=Table(data); tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightblue)]))
        elems.append(tbl); doc.build(elems); buf.seek(0)
        b64=base64.b64encode(buf.getvalue()).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">📥 Export PDF</a>', unsafe_allow_html=True)
    else:
        st.info("Žádná data k exportu.")

# --- Footer ---
st.markdown("---")
st.markdown(f"<div style='text-align:center;color:#888;'>Generováno {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
