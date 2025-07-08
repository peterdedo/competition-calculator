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

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        color: white;
        text-align: center;
        font-size: 1.3rem;
    }
    .phase-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.7rem 0 0.3rem 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
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
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
</div>
""", unsafe_allow_html=True)

# Výber varianty a typu jednotiek
st.markdown("""
<div class="variant-selector">
    <h3>Výběr varianty a typu jednotek</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    variant = st.radio(
        "Vyberte variantu:",
        ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
        horizontal=True
    )
with col2:
    unit_type = st.radio(
        "Vyberte typ jednotek:",
        ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
        horizontal=True
    )

# Kompletné dáta presne podľa tabuľky - vrátane všetkých aktivít pre fázy 4,5,6,7
activities_data = [
    # 1. Analytická fáze
    {"Fáze": "1. Analytická fáze", "Aktivita": "Sestavení řídící skupiny", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1, "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000,
     "Poznámka": "Zahájení projektu, definice cílů"},
    
    {"Fáze": "1. Analytická fáze", "Aktivita": "Vymezení řešeného území", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1, "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000,
     "Poznámka": "Definice hranic a rozsahu"},
    
    {"Fáze": "1. Analytická fáze", "Aktivita": "Seznámení se s dostupnými materiály a záměry v území", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6, "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
     "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000, "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000,
     "Poznámka": "Studium dokumentace a plánů"},
    
    {"Fáze": "1. Analytická fáze", "Aktivita": "Analýza stavu území na základě předem definovaných parametrů", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8, "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
     "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000, "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000,
     "Poznámka": "Terénní průzkum a analýza"},
    
    {"Fáze": "1. Analytická fáze", "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Zpracování analýzy do zadání"},
    
    {"Fáze": "1. Analytická fáze", "Aktivita": "Nalezení dohody aktérů (memorandum o shodě)", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4, "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000,
     "Poznámka": "Koordinace s dotčenými subjekty"},

    # 2. Přípravní fáze
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Návrh procesu soutěže (harmonogram, pracovní skupiny)", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5, "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000,
     "Poznámka": "Plánování průběhu soutěže"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Sestavení podrobného rozpočtu", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Detailní kalkulace nákladů"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Identifikace aktérů a návrh jejich zapojení", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4, "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000,
     "Poznámka": "Mapování zainteresovaných stran"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Komunikace s veřejností", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6, "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
     "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000, "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000,
     "Poznámka": "PR a osvěta"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Vytvoření značky soutěže", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Grafický design a branding"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "PR strategie projektu", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4, "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000,
     "Poznámka": "Komunikační strategie"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Kompletace zadání (včetně stavebního programu)", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 7, "MP jednotky - CZ": 7, "MP+TP jednotky - MEZ": 10.5, "MP+TP jednotky - CZ": 10.5,
     "Cena MP - MEZ": 98000, "Cena MP - CZ": 98000, "Cena MP+TP - MEZ": 147000, "Cena MP+TP - CZ": 147000,
     "Poznámka": "Vypracování soutěžních podmínek"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Formulace soutěžních podmínek", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5, "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000,
     "Poznámka": "Právní formulace podmínek"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Finalizace a publikace podmínek", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Publikace soutěžních podmínek"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Sestavení poroty", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Výběr a oslovení porotců"},
    
    {"Fáze": "2. Přípravní fáze", "Aktivita": "Ustavující schůze poroty", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1, "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000,
     "Poznámka": "První setkání poroty"},

    # 3. Průběh SW
    {"Fáze": "3. Průběh SW", "Aktivita": "Vyhlášení soutěže a výběr účastníků", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Výběr soutěžících týmů"},
    
    {"Fáze": "3. Průběh SW", "Aktivita": "Příprava a organizace 1. workshopu", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5, "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000,
     "Poznámka": "Organizace prvního workshopu"},
    
    {"Fáze": "3. Průběh SW", "Aktivita": "Příprava a organizace 2. workshopu", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5, "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000,
     "Poznámka": "Organizace druhého workshopu"},
    
    {"Fáze": "3. Průběh SW", "Aktivita": "Příprava a organizace 3. workshopu", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5, "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000,
     "Poznámka": "Organizace třetího workshopu"},

    # 4. Vyhlášení výsledků - KOMPLETNÉ AKTIVITY
    {"Fáze": "4. Vyhlášení výsledků", "Aktivita": "Hodnocení návrhů porotou", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4, "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000,
     "Poznámka": "Posouzení soutěžních návrhů"},
    
    {"Fáze": "4. Vyhlášení výsledků", "Aktivita": "Závěrečná schůze poroty", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Finální rozhodnutí poroty"},
    
    {"Fáze": "4. Vyhlášení výsledků", "Aktivita": "Vyhlášení výsledků soutěže", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1, "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000,
     "Poznámka": "Oficiální vyhlášení vítězů"},
    
    {"Fáze": "4. Vyhlášení výsledků", "Aktivita": "Ukončení soutěže a podpora další fáze", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Finalizace a předání výsledků"},

    # 5. PR podpora - KOMPLETNÉ AKTIVITY
    {"Fáze": "5. PR podpora", "Aktivita": "Tiskové zprávy a komunikace", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3, "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000,
     "Poznámka": "Mediální komunikace výsledků"},
    
    {"Fáze": "5. PR podpora", "Aktivita": "Vytvoření webových stránek", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Webová prezentace soutěže"},
    
    {"Fáze": "5. PR podpora", "Aktivita": "Vytvoření katalogu návrhů", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Tiskový katalog výsledků"},
    
    {"Fáze": "5. PR podpora", "Aktivita": "Organizace výstavy výsledků", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1, "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000,
     "Poznámka": "Výstava soutěžních návrhů"},

    # 6. Externí náklady - KOMPLETNÉ AKTIVITY
    {"Fáze": "6. Externí náklady", "Aktivita": "Ubytování účastníků a porotců", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4, "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000,
     "Poznámka": "Ubytovací služby"},
    
    {"Fáze": "6. Externí náklady", "Aktivita": "Překlady materiálů", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Jazykové překlady"},
    
    {"Fáze": "6. Externí náklady", "Aktivita": "Grafické práce a tisk", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "Grafický design a tisk"},
    
    {"Fáze": "6. Externí náklady", "Aktivita": "Webové služby a IT podpora", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2, "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
     "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000,
     "Poznámka": "IT a webové služby"},

    # 7. Odměny - KOMPLETNÉ AKTIVITY
    {"Fáze": "7. Odměny", "Aktivita": "Odměny porotcům", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8, "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
     "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000, "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000,
     "Poznámka": "Odměny pro členy poroty"},
    
    {"Fáze": "7. Odměny", "Aktivita": "Odměny účastníkům soutěže", "Jednotka": "den", "Cena za jednotku": 14000,
     "MP jednotky - MEZ": 7, "MP jednotky - CZ": 7, "MP+TP jednotky - MEZ": 10.5, "MP+TP jednotky - CZ": 10.5,
     "Cena MP - MEZ": 98000, "Cena MP - CZ": 98000, "Cena MP+TP - MEZ": 147000, "Cena MP+TP - CZ": 147000,
     "Poznámka": "Odměny pro soutěžící týmy"}
]

df = pd.DataFrame(activities_data)
fazes = df["Fáze"].unique()

selected_activities = []
total = 0
selected_count = 0
total_activities = len(df)

# Kľúče podľa výberu
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"

# Zobrazenie len vybraného variantu a typu jednotiek
st.markdown("---")
st.markdown(f"<div class='main-header'><h2>Aktivity pro {variant} - {unit_type}</h2></div>", unsafe_allow_html=True)

for faze in fazes:
    st.markdown(f"<div class='phase-header'>{faze}</div>", unsafe_allow_html=True)
    faze_df = df[df["Fáze"] == faze]
    faze_total = 0

    for i, row in faze_df.iterrows():
        with st.expander(f"{row['Aktivita']}", expanded=False):
            jednotky_key = f"{ukey} jednotky - {vkey}"
            cena_key = f"Cena {ukey} - {vkey}"
            jednotky_default = row.get(jednotky_key, 0) or 0
            cena_za_aktivitu = row.get(cena_key, 0) or 0
            cena_za_jednotku = row.get("Cena za jednotku", 0) or 0
            if jednotky_default and cena_za_aktivitu:
                cena_za_jednotku = int(cena_za_aktivitu / jednotky_default)
            
            jednotky = st.number_input(
                "Jednotek",
                min_value=0,
                value=int(jednotky_default),
                key=f"units_{faze}_{i}_{row['Aktivita'].replace(' ', '_')}_{jednotky_key}"
            )
            subtotal = jednotky * cena_za_jednotku
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Jednotka:** {row['Jednotka']}")
                st.write(f"**Cena za jednotku:** {cena_za_jednotku:,} Kč")
            with col2:
                st.write(f"**Subtotal:** {subtotal:,} Kč")
                if row.get("Poznámka"):
                    st.info(f"**Poznámka:** {row['Poznámka']}")
            
            if jednotky > 0:
                selected_activities.append({
                    "Fáze": faze,
                    "Aktivita": row['Aktivita'],
                    "Jednotka": row['Jednotka'],
                    "Množství": jednotky,
                    "Cena za jednotku": cena_za_jednotku,
                    "Subtotal": subtotal,
                    "Poznámka": row.get("Poznámka", "")
                })
                faze_total += subtotal
                total += subtotal
                selected_count += 1
    
    if faze_total > 0:
        st.markdown(f"<div class='metric-card'><strong>{faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)

# Progress bar
progress = selected_count / total_activities if total_activities else 0
st.progress(progress, text=f"Pokrok: {selected_count}/{total_activities} aktivit vybráno")

# Grafy
if selected_activities:
    st.markdown("---")
    st.markdown("<div class='main-header'><h2>Vizualizace nákladů</h2></div>", unsafe_allow_html=True)
    df_selected = pd.DataFrame(selected_activities)
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            df_selected.groupby('Fáze')['Subtotal'].sum().reset_index(),
            values='Subtotal',
            names='Fáze',
            title='Rozložení nákladů podle fází'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(
            df_selected,
            x='Aktivita',
            y='Subtotal',
            color='Fáze',
            title='Náklady podle aktivit'
        )
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)

# Celkové výsledky
st.markdown("---")
st.markdown("<div class='main-header'><h2>Celkové náklady</h2></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h3>Celková suma bez DPH</h3><h2>{total:,} Kč</h2></div>", unsafe_allow_html=True)
with col2:
    vat_amount = total * 0.21
    st.markdown(f"<div class='metric-card'><h3>DPH (21%)</h3><h2>{vat_amount:,} Kč</h2></div>", unsafe_allow_html=True)
with col3:
    total_with_vat = total * 1.21
    st.markdown(f"<div class='metric-card'><h3>Celková suma s DPH</h3><h2>{total_with_vat:,} Kč</h2></div>", unsafe_allow_html=True)

# Detailný prehľad a export
if selected_activities:
    st.markdown("---")
    st.markdown("<div class='main-header'><h2>Detailní přehled aktivit</h2></div>", unsafe_allow_html=True)
    df_selected = pd.DataFrame(selected_activities)
    st.dataframe(df_selected, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='main-header'><h2>Export výsledků</h2></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export do Excel"):
            df_selected.to_excel("soutezni_workshop_rozpocet.xlsx", index=False)
            st.success("Rozpočet byl exportován do 'soutezni_workshop_rozpocet.xlsx'")
    with col2:
        if st.button("Export do PDF"):
            def generate_pdf_report(df_data, total_data):
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                elements = []
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=1
                )
                elements.append(Paragraph("Kalkulátor soutěžního workshopu", title_style))
                elements.append(Spacer(1, 20))
                elements.append(Paragraph("Celkové náklady:", styles['Heading2']))
                elements.append(Spacer(1, 10))
                summary_data = [
                    ['Popis', 'Částka (Kč)'],
                    ['Celková suma bez DPH', f"{total_data['total']:,}"],
                    ['DPH (21%)', f"{total_data['vat']:,}"],
                    ['Celková suma s DPH', f"{total_data['total_with_vat']:,}"]
                ]
                summary_table = Table(summary_data)
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(summary_table)
                elements.append(Spacer(1, 20))
                elements.append(Paragraph("Detailní přehled aktivit:", styles['Heading2']))
                elements.append(Spacer(1, 10))
                table_data = [['Fáze', 'Aktivita', 'Jednotka', 'Množství', 'Cena za jednotku', 'Subtotal', 'Poznámka']]
                for _, row in df_data.iterrows():
                    table_data.append([
                        row['Fáze'],
                        row['Aktivita'],
                        row['Jednotka'],
                        str(row['Množství']),
                        f"{row['Cena za jednotku']:,}",
                        f"{row['Subtotal']:,}",
                        row.get('Poznámka', '')
                    ])
                max_rows_per_page = 25
                for i in range(0, len(table_data), max_rows_per_page):
                    page_data = table_data[i:i + max_rows_per_page]
                    if i > 0:
                        elements.append(Spacer(1, 20))
                    table = Table(page_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    elements.append(table)
                doc.build(elements)
                buffer.seek(0)
                return buffer
            total_data = {
                'total': total,
                'vat': vat_amount,
                'total_with_vat': total_with_vat
            }
            pdf_buffer = generate_pdf_report(df_selected, total_data)
            b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="soutezni_workshop_rozpocet.pdf">Stáhnout PDF report</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("PDF report byl úspěšně vygenerován!")

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #666; padding: 2rem;'>Kalkulátor soutěžního workshopu | {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>", unsafe_allow_html=True)
