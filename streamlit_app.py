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
# Reset functionality removed to avoid AttributeError

# ------- Load Data (from CSV) -------
from io import StringIO

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Import aktivit")
uploaded_file = st.sidebar.file_uploader(
    "Nahrajte CSV soubor s aktivitami",
    type=["csv"],
    help="CSV by mělo mít sloupce: Fáze,Aktivita,Jednotka,Cena za jednotku,MP jednotky - MEZ,MP jednotky - CZ,MP+TP jednotky - MEZ,MP+TP jednotky - CZ"
)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info("Pro správné fungování nahrajte CSV s aktivitami.")
    st.stop()

# Ensure correct typing
numeric_cols = ['Cena za jednotku', 'MP jednotky - MEZ', 'MP jednotky - CZ', 'MP+TP jednotky - MEZ', 'MP+TP jednotky - CZ']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

vkey = "MEZ" if variant.startswith("Mezinárodní") else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# Load dataframe complete

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
