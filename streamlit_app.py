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
  .sidebar .stNumberInput label, .sidebar .stRadio label, .sidebar .stSelectBox label { font-weight: 500; }
  .btn-download { margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ------- Sidebar Controls -------
st.sidebar.header("⚙️ Parametry kalkulace")
variant = st.sidebar.selectbox(
    "Varianta soutěže:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    index=0
)
unit_type = st.sidebar.selectbox(
    "Typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
    index=0
)
search_term = st.sidebar.text_input("🔍 Filtr aktivit")
phases = [
    'Analytická fáze', 'Přípravní fáze', 'Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW', 'PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé', 'Odměny'
]
phases_filter = st.sidebar.multiselect(
    "Fáze k zobrazení:", phases, default=phases
)
# Reset filters
if st.sidebar.button("🔄 Resetovat filtry"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# ------- Load Data -------
@st.experimental_memo
def load_data():
    activities_data = [
        # ... (all activities entries) ...
    ]  # end of activities_data list
    return pd.DataFrame(activities_data)  # ensure closure of list and return
", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 6.0, "MP+TP jednotky - CZ": 6.0},
        # Přípravní fáze
        {"Fáze": "Přípravní fáze", "Aktivita": "Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 15.0, "MP jednotky - CZ": 15.0, "MP+TP jednotky - MEZ": 20.0, "MP+TP jednotky - CZ": 20.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení podrobného rozpočtu", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 2.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 3.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 10.0, "MP jednotky - CZ": 10.0, "MP+TP jednotky - MEZ": 15.0, "MP+TP jednotky - CZ": 15.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 0.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 15.0, "MP+TP jednotky - CZ": 15.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Vytvoření značky soutěže (včetně konzultace se zadavatelem)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 4.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "PR strategie projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 3.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace zadání (parametry využití území, stavební program, průběžná jednání s ŘS a PS)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 50.0, "MP+TP jednotky - CZ": 40.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Formulace soutěžních podmínek", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 16.0, "MP jednotky - CZ": 16.0, "MP+TP jednotky - MEZ": 20.0, "MP+TP jednotky - CZ": 20.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Finalizace a publikace soutěžních podmínek a zadání", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 5.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení poroty", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 6.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 9.0, "MP+TP jednotky - CZ": 8.0},
        {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace před vyhlášením soutěže a ustavující schůze poroty (včetně regulérnosti ČKA)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 23.0, "MP jednotky - CZ": 23.0, "MP+TP jednotky - MEZ": 25.0, "MP+TP jednotky - CZ": 25.0},
        # Průběh soutěžního workshopu (SW)
        {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Vyhlášení soutěže – otevřená výzva a výběr soutěžících", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 7.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 7.0, "MP+TP jednotky - CZ": 5.0},
        {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 1. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0},
        {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 2. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0},
        {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 3. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0},
        # Vyhlášení výsledků SW
        {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Procesní ukončení soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0},
        {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Podpora v navazujících fázích projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 10.0, "MP+TP jednotky - CZ": 10.0},
        # PR podpora v průběhu celé soutěže
        {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná komunikace projektu (včetně tiskových zpráv)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 17.0, "MP jednotky - CZ": 13.0, "MP+TP jednotky - MEZ": 17.0, "MP+TP jednotky - CZ": 13.0},
        {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná aktualizace webu", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0},
        {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Soutěžní katalog (struktura, obsah)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 4.0},
        {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Výstava vítězních návrhů (příprava, struktura, obsah, produkční zajištění, instalace)", "Jednotka": "den", "Cena za jednotku": 14000.0,
         "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 5.0},
        # Další náklady - externí dodavatelé
        {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Produkcční náklady SW (pronájmy sálů pro SW, tisk, občerstvení, technické zajištění)", "Jednotka": "SW", "Cena za jednotku": 60000.0,
         "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0},
        {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Ubytování zahraničních porotců", "Jednotka": "noc", "Cena za jednotku": 5500.0,
         "MP jednotky - MEZ": 9.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 9.0, "MP+TP jednotky - CZ": 0.0},
        {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Cestovné pro zahraniční porotce", "Jednotka": "cesta", "Cena za jednotku": 7000.0,
         "MP jednot...


df = load_data()
vkey = "MEZ" if variant.startswith("Mezinárodní") else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# ------- Prepare filtered df and total_inputs -------
filtered = df[df['Fáze'].isin(phases_filter)]
if search_term:
    filtered = filtered[filtered['Aktivita'].str.contains(search_term, case=False, na=False)]
total_inputs = len(filtered)

# ------- Main Header -------
st.markdown(
    f"<div class='header'><h1>Kalkulátor soutěžního workshopu</h1>"
    f"<p>Varianta: {variant} | Jednotky: {unit_type}</p></div>",
    unsafe_allow_html=True
)

# ------- Activity Inputs -------
sel = []
progress_bar = st.progress(0)
processed = 0
for phase in phases:
    if phase not in phases_filter: continue
    phase_df = filtered[filtered['Fáze'] == phase]
    if phase_df.empty: continue
    st.markdown(f"<div class='subheader'>{phase}</div>", unsafe_allow_html=True)
    for idx, row in phase_df.iterrows():
        key = f"unit_{idx}"
        default = row.get(f"{ukey} jednotky - {vkey}", 0) or 0
        cols = st.columns([3,1])
        units = cols[0].number_input(
            row['Aktivita'], value=float(default), step=0.5, min_value=0.0, key=key
        )
        subtotal = units * float(row['Cena za jednotku'])
        cols[1].markdown(f"**{subtotal:,.0f} Kč**")
        if units > 0:
            sel.append({
                'Fáze': phase,
                'Aktivita': row['Aktivita'],
                'Jednotka': row['Jednotka'],
                'Množství': units,
                'Cena': row['Cena za jednotku'],
                'Celkem': subtotal
            })
        processed += 1
        progress_bar.progress(processed/total_inputs)

# ------- Summary and Tabs -------
if sel:
    df_sel = pd.DataFrame(sel)
    total = df_sel['Celkem'].sum()
    vat = total * 0.21
    total_vat = total + vat
    tabs = st.tabs(["Souhrn", "Vizualizace", "Export"])

    with tabs[0]:
        st.markdown("<div class='subheader'>Souhrn nákladů</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h4>Bez DPH</h4><h2>{total:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h4>DPH 21%</h4><h2>{vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h4>S DPH</h4><h2>{total_vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        st.table(df_sel.groupby('Fáze')['Celkem'].sum().reset_index().rename(columns={'Celkem':'Částka'}))

    with tabs[1]:
        st.markdown("<div class='subheader'>Grafy</div>", unsafe_allow_html=True)
        pie = px.pie(df_sel.groupby('Fáze')['Celkem'].sum().reset_index(), names='Fáze', values='Celkem')
        bar = px.bar(df_sel, x='Aktivita', y='Celkem', color='Fáze')
        bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(pie, use_container_width=True)
        st.plotly_chart(bar, use_container_width=True)

    with tabs[2]:
        st.markdown("<div class='subheader'>Export</div>", unsafe_allow_html=True)
        csv = df_sel.to_csv(index=False).encode('utf-8')
        st.download_button("📥 CSV", data=csv, file_name="rozpocet.csv", mime='text/csv', css_class='btn-download')
        # PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elems = [Paragraph("Kalkulátor soutěžního workshopu", getSampleStyleSheet()['Heading1']), Spacer(1,12)]
        data = [['Fáze','Aktivita','Jednotka','Množství','Cena','Celkem']]
        for r in sel:
            data.append([r['Fáze'], r['Aktivita'], r['Jednotka'], r['Množství'], f"{r['Cena']:,.0f}", f"{r['Celkem']:,.0f}"])
        tbl = Table(data)
        tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightblue)]))
        elems.append(tbl)
        doc.build(elems)
        buffer.seek(0)
        st.download_button("📥 PDF", data=buffer, file_name="rozpocet.pdf", mime='application/pdf', css_class='btn-download')

# ------- Footer -------
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:#888;'>Gen: {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
