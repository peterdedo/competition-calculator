import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Page Config & Styling ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon=":cityscape:", layout="wide")
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
  body { background: #f4f4f4; font-family: 'Montserrat', sans-serif; }
  .main-header { background: linear-gradient(135deg,#2c3e50,#34495e); padding:2rem; border-radius:10px;
                 color:#ecf0f1; text-align:center; font-size:2.4rem; font-weight:800; box-shadow:0 4px 16px rgba(0,0,0,0.2);
                 margin-bottom:2rem; }
  .phase-header { background:#27ae60; padding:0.8rem 1rem; border-radius:6px; color:#fff;
                   margin-top:1.5rem; font-weight:700; display:flex; align-items:center; gap:0.5rem; }
  .metric-card { background:#ecf0f1; padding:1rem; border-radius:10px;
                  text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.1); color:#2c3e50; margin-bottom:1rem; }
  .subheader { color:#2c3e50; font-size:1.4rem; font-weight:600; margin-top:2.5rem; }
  .metric-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1rem; margin:2rem 0; }
  .footer { text-align:center; color:#95a5a6; padding:2rem 0; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_activities(path='Strukturovan__nab_dka.csv'):
    for p in [path, '/mount/data/Strukturovan__nab_dka.csv', '/mnt/data/Strukturovan__nab_dka.csv']:
        try:
            df = pd.read_csv(p, sep=',', encoding='utf-8', skipinitialspace=True)
        except FileNotFoundError:
            continue
        except pd.errors.ParserError:
            try:
                df = pd.read_csv(p, sep=';', encoding='utf-8', skipinitialspace=True)
            except Exception:
                continue
        # Remove unnamed first column
        if df.columns[0].lower().startswith('unnamed') or df.columns[0] == '':
            df = df.iloc[:, 1:]
        st.sidebar.info(f"Načteno z {p}")
        return df
    st.error("Nepodařilo se najít nebo načíst soubor s daty aktivit.")
    st.stop()

df = load_activities()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Nastavení workshopu")
    variant = st.selectbox("Variant workshopu:", ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"])
    unit_type = st.selectbox("Typ jednotek:", ["MP", "MP + TP"])
    search = st.text_input("🔍 Hledat aktivitu:")
    phases = st.multiselect("🗂️ Vyber fáze:", df["Fáze"].unique(), default=df["Fáze"].unique())

# --- Header ---
st.markdown('<div class="main-header">Kalkulátor soutěžního workshopu</div>', unsafe_allow_html=True)

# --- Filter & Keys ---
df = df[df["Fáze"].isin(phases)]
if search:
    df = df[df["Aktivita"].str.contains(search, case=False, na=False)]
vkey = "MEZ" if variant.startswith("Mezinárodní") else "CZ"
ukey = unit_type.replace(" ", "") + " jednotky"
unit_col = f"{ukey} - {vkey}"

# --- Quantity Input Table ---
df = df.rename(columns={unit_col: 'Množství'})
df['Množství'] = df['Množství'].fillna(0)
edited = st.experimental_data_editor(df[['Fáze','Aktivita','Jednotka','Cena za jednotku','Množství']], num_rows="dynamic")

# --- Calculate Costs ---
edited['Cena'] = edited['Množství'] * edited['Cena za jednotku']
selected = edited[edited['Množství'] > 0]
total = selected['Cena'].sum()

# --- Phase Summaries ---
for phase, subdf in selected.groupby('Fáze'):
    phase_sum = subdf['Cena'].sum()
    st.markdown(f'<div class="phase-header">🏙️ {phase} — {phase_sum:,.0f} Kč</div>', unsafe_allow_html=True)

# --- Progress ---
st.progress(min(len(selected) / max(len(df), 1), 1.0))

# --- Visualizations ---
if not selected.empty:
    st.markdown('<div class="subheader">Vizualizace nákladů</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.pie(
            selected.groupby('Fáze')['Cena'].sum().reset_index(),
            names='Fáze', values='Cena', hole=0.4
        ),
        use_container_width=True
    )
    c2.plotly_chart(
        px.bar(selected, x='Aktivita', y='Cena', color='Fáze').update_layout(xaxis_tickangle=45),
        use_container_width=True
    )

# --- Summary & Footer ---
vat = total * 0.21
tot_vat = total + vat
with st.container():
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    for title, val in [('Bez DPH', total), ('DPH 21%', vat), ('S DPH', tot_vat)]:
        st.markdown(f'<div class="metric-card"><h3>{title}</h3><h2>{val:,.0f} Kč</h2></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<div class='footer'>Aktualizováno: {datetime.now():%d.%m.%Y %H:%M}</div>", unsafe_allow_html=True)
