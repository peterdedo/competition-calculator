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
        # (zde vložte kompletní seznam aktivit jako původně)
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
