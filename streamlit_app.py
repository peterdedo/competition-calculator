import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ------- Page Config -------
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------- Styling -------
st.markdown("""
<style>
  .header { background: linear-gradient(90deg, #667eea, #764ba2); padding: 1rem; border-radius: 0.5rem; color: #fff; text-align: center; }
  .subheader { font-size: 1.2rem; margin-top: 1.5rem; font-weight: 600; }
  .metric-card { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1rem; border-radius: 1rem; color: #fff; text-align: center; }
  .btn-download { margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ------- Sidebar -------
st.sidebar.header("⚙️ Parametry kalkulace")
variant = st.sidebar.selectbox(
    "Varianta soutěže:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"]
)
unit_choice = st.sidebar.selectbox(
    "Typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"]
)
search_term = st.sidebar.text_input("🔍 Filtr aktivit")
phases = [
    'Analytická fáze',
    'Přípravní fáze',
    'Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW',
    'PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé',
    'Odměny'
]
show_phases = st.sidebar.multiselect("Fáze k zobrazení:", phases, default=phases)

# ------- Data -------
def load_data():
    data = [
        # (all previous entries...)
        {"Fáze":"Přípravní fáze","Aktivita":"Sestavení poroty","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":6,"MP jednotky - CZ":5,"MP+TP jednotky - MEZ":9,"MP+TP jednotky - CZ":8},
        # Continue with remaining entries following the same structure...
    ]  # <-- ensure the list is closed here
    return pd.DataFrame(data)

def main():
    df = load_data()
    vkey = "MEZ" if variant.startswith("Mezinárodní") else "CZ"
    ukey = "MP" if "MP)" in unit_choice else "MP+TP"

    # Filter by phase and search
    df = df[df['Fáze'].isin(show_phases)]
    if search_term:
        df = df[df['Aktivita'].str.contains(search_term, case=False, na=False)]

    # Inputs
    selected = []
    progress = st.progress(0)
    for i, row in df.iterrows():
        cols = st.columns([3,1])
        units = cols[0].number_input(
            f"{row['Fáze']} – {row['Aktivita']}",
            value=float(row[f"{ukey} jednotky - {vkey}"]),
            step=0.5,
            min_value=0.0,
            key=f"unit_{i}"
        )
        subtotal = units * row['Cena za jednotku']
        cols[1].markdown(f"**{subtotal:,.0f} Kč**")
        if units > 0:
            selected.append({
                'Fáze': row['Fáze'],
                'Aktivita': row['Aktivita'],
                'Jednotka': row['Jednotka'],
                'Množství': units,
                'Cena': row['Cena za jednotku'],
                'Subtotal': subtotal
            })
        progress.progress((i+1)/len(df))

    # Summary and export
    if selected:
        sel_df = pd.DataFrame(selected)
        total = sel_df['Subtotal'].sum()
        vat = total * 0.21
        total_vat = total + vat

        st.markdown("---")
        st.markdown("<div class='subheader'>Celkové náklady</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card'><h4>Bez DPH</h4><h2>{total:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><h4>DPH 21%</h4><h2>{vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><h4>S DPH</h4><h2>{total_vat:,.0f} Kč</h2></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.dataframe(sel_df)

        csv = sel_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv, file_name="rozpocet.csv", mime='text/csv', css_class='btn-download')

        # PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elems = [Paragraph("Kalkulátor soutěžního workshopu", getSampleStyleSheet()['Heading1']), Spacer(1,12)]
        table_data = [['Fáze','Aktivita','Jednotka','Množství','Cena','Subtotal']]
        for _, r in sel_df.iterrows():
            table_data.append([r['Fáze'], r['Aktivita'], r['Jednotka'], r['Množství'], f"{r['Cena']:,.0f}", f"{r['Subtotal']:,.0f}"])
        tbl = Table(table_data)
        tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.5,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightblue)]))
        elems.append(tbl)
        doc.build(elems)
        buffer.seek(0)
        st.download_button("📥 Export PDF", data=buffer, file_name="rozpocet.pdf", mime='application/pdf', css_class='btn-download')

if __name__ == "__main__":
    main()
