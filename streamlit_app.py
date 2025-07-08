import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ------- Page Config -------
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------- Custom CSS Styling -------
st.markdown("""
<style>
  /* Headers */
  .header { background: linear-gradient(90deg, #667eea, #764ba2); padding: 1rem; border-radius: 0.5rem; color: white; text-align: center; }
  .subheader { font-size: 1.2rem; margin-top: 1.5rem; font-weight: 600; }
  /* Metrics */
  .metric-card { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1rem; border-radius: 1rem; color: white; text-align: center; }
  /* Sidebar inputs */
  .sidebar .stNumberInput label, .sidebar .stRadio label { font-weight: 500; }
  .btn-download { margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ------- Sidebar Controls -------
st.sidebar.header("⚙️ Parametry kalkulace")
variant = st.sidebar.selectbox(
    "Varianta soutěže:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"]
)
unit_type = st.sidebar.selectbox(
    "Typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"]
)
search_term = st.sidebar.text_input("🔍 Filtr aktivit", "")
phases = [
    'Analytická fáze','Přípravní fáze','Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW','PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé','Odměny'
]
phases_filter = st.sidebar.multiselect(
    "Fáze k zobrazení:", phases, default=phases
)
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Resetovat všechny"): st.experimental_rerun()

# ------- Load Data and Prepare Keys -------
@st.experimental_memo
def load_data():
    activities_data = [
        # Analytická fáze
        {"Fáze": "Analytická fáze", "Aktivita": "Sestavení řídící skupiny", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 2.0, "MP+TP jednotky - CZ": 2.0},
        {"Fáze": "Analytická fáze", "Aktivita": "Vymezení řešeného území", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 2.0, "MP+TP jednotky - CZ": 2.0},
        {"Fáze": "Analytická fáze", "Aktivita": "Seznámení se s dostupnými materiály a záměry v území", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 6.0, "MP jednotky - CZ": 6.0, "MP+TP jednotky - MEZ": 8.0, "MP+TP jednotky - CZ": 8.0},
        {"Fáze": "Analytická fáze", "Aktivita": "Analýza stavu území na základě předem definovaných parametrů a indikátorů", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 32.0, "MP jednotky - CZ": 32.0, "MP+TP jednotky - MEZ": 42.0, "MP+TP jednotky - CZ": 42.0},
        {"Fáze": "Analytická fáze", "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 8.0, "MP jednotky - CZ": 8.0, "MP+TP jednotky - MEZ": 11.0, "MP+TP jednotky - CZ": 11.0},
        {"Fáze": "Analytická fáze", "Aktivita": "Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 6.0, "MP+TP jednotky - CZ": 6.0},
        # (include all phases and activities similarly...)
        # Přípravní fáze, Průběh SW, Vyhlášení výsledků, PR podpora, Další náklady, Odměny
    ]
    return pd.DataFrame(activities_data)

df = load_data()
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# ------- Main Header -------
st.markdown(f"<div class='header'><h1>Kalkulátor soutěžního workshopu</h1><p>Varianta: {variant} | Jednotky: {unit_type}</p></div>", unsafe_allow_html=True)

# ------- Activity Inputs -------
sel = []
st.progress(0, text="Načítám...")
count = 0; total_inputs = 0
for phase in phases:
    if phase not in phases_filter: continue
    st.markdown(f"<div class='subheader'>{phase}</div>", unsafe_allow_html=True)
    phase_df = df[df['Fáze']==phase]
    for idx, row in phase_df.iterrows():
        label = row['Aktivita']
        if search_term and search_term.lower() not in label.lower(): continue
        key = f"unit_{phase}_{idx}"
        default = float(row.get(f"{ukey} jednotky - {vkey}", 0) or 0)
        col1, col2 = st.columns([3,1])
        with col1:
            units = st.number_input(label, min_value=0.0, value=default, step=0.5, key=key)
        price = float(row['Cena za jednotku'])
        subtotal = units * price
        with col2:
            st.write(f"**{subtotal:,.0f} Kč**")
        total_inputs += 1
        if units > 0:
            sel.append({
                'Fáze': phase,
                'Aktivita': label,
                'Jednotka': row['Jednotka'],
                'Množství': units,
                'Cena': price,
                'Celkem': subtotal
            })
        count += 1
        st.progress(count/total_inputs, text=f"Zpracováno {count}/{total_inputs}")

# ------- Summary and Tabs -------
if sel:
    df_sel = pd.DataFrame(sel)
    total = df_sel['Celkem'].sum()
    vat = total * 0.21
    total_vat = total + vat
    tab1, tab2, tab3 = st.tabs(["Souhrn", "Vizualizace", "Export"])

    with tab1:
        st.markdown("<div class='subheader'>Souhrn nákladů</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h4>Celkem bez DPH</h4><h2>{total:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h4>DPH 21%</h4><h2>{vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h4>Celkem s DPH</h4><h2>{total_vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        st.table(df_sel.groupby('Fáze')['Celkem'].sum().rename("Částka").reset_index())

    with tab2:
        st.markdown("<div class='subheader'>Grafy</div>", unsafe_allow_html=True)
        fig1 = px.pie(df_sel.groupby('Fáze')['Celkem'].sum().reset_index(), names='Fáze', values='Částka', title="Rozdělení podle fází")
        fig2 = px.bar(df_sel, x='Aktivita', y='Celkem', color='Fáze', title="Náklady dle aktivity")
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.markdown("<div class='subheader'>Export</div>", unsafe_allow_html=True)
        csv = df_sel.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv, file_name="rozpocet.csv", mime='text/csv', css_class='btn-download')
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elems = [Paragraph("Kalkulátor soutěžního workshopu", getSampleStyleSheet()['Heading1']), Spacer(1,12)]
        data = [['Fáze','Aktivita','Jednotka','Množství','Cena','Celkem']] + [[
            r['Fáze'], r['Aktivita'], r['Jednotka'], r['Množství'], f"{r['Cena']:,.0f}", f"{r['Celkem']:,.0f}"
        ] for _, r in df_sel.iterrows()]
        tbl = Table(data)
        tbl.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.grey), ('BACKGROUND', (0,0), (-1,0), colors.lightblue)]))
        elems.append(tbl)
        doc.build(elems)
        buffer.seek(0)
        st.download_button("📥 Export PDF", data=buffer, file_name="rozpocet.pdf", mime='application/pdf', css_class='btn-download')

# ------- Footer -------
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#888;'>Generováno: {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
