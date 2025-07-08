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

# Presné dáta z textového súboru
activities_data = [
    # Analytická fáze
    {"Fáze": "Analytická fáze", "Aktivita": "Sestavení řídící skupiny", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 2.0, "MP+TP jednotky - CZ": 2.0,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 28000, "Cena MP+TP - CZ": 28000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Vymezení řešeného území", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 2.0, "MP+TP jednotky - CZ": 2.0,
     "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000, "Cena MP+TP - MEZ": 28000, "Cena MP+TP - CZ": 28000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Seznámení se s dostupnými materiály a záměry v území", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 6.0, "MP jednotky - CZ": 6.0, "MP+TP jednotky - MEZ": 8.0, "MP+TP jednotky - CZ": 8.0,
     "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000, "Cena MP+TP - MEZ": 112000, "Cena MP+TP - CZ": 112000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Analýza stavu území na základě předem definovaných parametrů a indikátorů", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 32.0, "MP jednotky - CZ": 32.0, "MP+TP jednotky - MEZ": 42.0, "MP+TP jednotky - CZ": 42.0,
     "Cena MP - MEZ": 448000, "Cena MP - CZ": 448000, "Cena MP+TP - MEZ": 588000, "Cena MP+TP - CZ": 588000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 8.0, "MP jednotky - CZ": 8.0, "MP+TP jednotky - MEZ": 11.0, "MP+TP jednotky - CZ": 11.0,
     "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000, "Cena MP+TP - MEZ": 154000, "Cena MP+TP - CZ": 154000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 6.0, "MP+TP jednotky - CZ": 6.0,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000},

    # Přípravní fáze
    {"Fáze": "Přípravní fáze", "Aktivita": "Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 15.0, "MP jednotky - CZ": 15.0, "MP+TP jednotky - MEZ": 20.0, "MP+TP jednotky - CZ": 20.0,
     "Cena MP - MEZ": 210000, "Cena MP - CZ": 210000, "Cena MP+TP - MEZ": 280000, "Cena MP+TP - CZ": 280000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení podrobného rozpočtu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 2.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 28000, "Cena MP+TP - MEZ": 56000, "Cena MP+TP - CZ": 42000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 10.0, "MP jednotky - CZ": 10.0, "MP+TP jednotky - MEZ": 15.0, "MP+TP jednotky - CZ": 15.0,
     "Cena MP - MEZ": 140000, "Cena MP - CZ": 140000, "Cena MP+TP - MEZ": 210000, "Cena MP+TP - CZ": 210000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 0.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 15.0, "MP+TP jednotky - CZ": 15.0,
     "Cena MP - MEZ": 0, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 210000, "Cena MP+TP - CZ": 210000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Vytvoření značky soutěže (včetně konzultace se zadavatelem)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 4.0,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 56000, "Cena MP+TP - CZ": 56000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "PR strategie projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 4.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 56000, "Cena MP+TP - CZ": 42000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace zadání (parametry využití území, stavební program, průběžná jednání s ŘS a PS)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 50.0, "MP+TP jednotky - CZ": 40.0,
     "Cena MP - MEZ": 420000, "Cena MP - CZ": 350000, "Cena MP+TP - MEZ": 700000, "Cena MP+TP - CZ": 560000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Formulace soutěžních podmínek", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 16.0, "MP jednotky - CZ": 16.0, "MP+TP jednotky - MEZ": 20.0, "MP+TP jednotky - CZ": 20.0,
     "Cena MP - MEZ": 224000, "Cena MP - CZ": 224000, "Cena MP+TP - MEZ": 280000, "Cena MP+TP - CZ": 280000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Finalizace a publikace soutěžních podmínek a zadání", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 4.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 5.0,
     "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 70000, "Cena MP+TP - CZ": 70000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení poroty", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 6.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 9.0, "MP+TP jednotky - CZ": 8.0,
     "Cena MP - MEZ": 84000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 112000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace před vyhlášením soutěže a ustavující schůze poroty (včetně regulérnosti ČKA)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 23.0, "MP jednotky - CZ": 23.0, "MP+TP jednotky - MEZ": 25.0, "MP+TP jednotky - CZ": 25.0,
     "Cena MP - MEZ": 322000, "Cena MP - CZ": 322000, "Cena MP+TP - MEZ": 350000, "Cena MP+TP - CZ": 350000},

    # Průběh soutěžního workshopu (SW)
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Vyhlášení soutěže – otevřená výzva a výběr soutěžících", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 7.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 7.0, "MP+TP jednotky - CZ": 5.0,
     "Cena MP - MEZ": 98000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 98000, "Cena MP+TP - CZ": 70000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 1. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0,
     "Cena MP - MEZ": 420000, "Cena MP - CZ": 350000, "Cena MP+TP - MEZ": 420000, "Cena MP+TP - CZ": 350000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 2. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0,
     "Cena MP - MEZ": 420000, "Cena MP - CZ": 350000, "Cena MP+TP - MEZ": 420000, "Cena MP+TP - CZ": 350000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 3. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 30.0, "MP jednotky - CZ": 25.0, "MP+TP jednotky - MEZ": 30.0, "MP+TP jednotky - CZ": 25.0,
     "Cena MP - MEZ": 420000, "Cena MP - CZ": 350000, "Cena MP+TP - MEZ": 420000, "Cena MP+TP - CZ": 350000},

    # Vyhlášení výsledků SW
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Procesní ukončení soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000},
    
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Podpora v navazujících fázích projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 10.0, "MP+TP jednotky - CZ": 10.0,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 140000, "Cena MP+TP - CZ": 140000},

    # PR podpora v průběhu celé soutěže
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná komunikace projektu (včetně tiskových zpráv)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 17.0, "MP jednotky - CZ": 13.0, "MP+TP jednotky - MEZ": 17.0, "MP+TP jednotky - CZ": 13.0,
     "Cena MP - MEZ": 238000, "Cena MP - CZ": 182000, "Cena MP+TP - MEZ": 238000, "Cena MP+TP - CZ": 182000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná aktualizace webu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000, "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Soutěžní katalog (struktura, obsah)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 4.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 4.0,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 56000, "Cena MP+TP - MEZ": 70000, "Cena MP+TP - CZ": 56000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Výstava vítězních návrhů (příprava, struktura, obsah, produkční zajištění, instalace)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 5.0,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 70000, "Cena MP+TP - CZ": 70000},

    # Další náklady - externí dodavatelé
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Produkcční náklady SW (pronájmy sálů pro SW, tisk, občerstvení, technické zajištění)", "Jednotka": "SW", "Cena za jednotku": 60000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 180000, "Cena MP - CZ": 180000, "Cena MP+TP - MEZ": 180000, "Cena MP+TP - CZ": 180000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Ubytování zahraničních porotců", "Jednotka": "noc", "Cena za jednotku": 5500.0,
     "MP jednotky - MEZ": 9.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 9.0, "MP+TP jednotky - CZ": 0.0,
     "Cena MP - MEZ": 49500, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 49500, "Cena MP+TP - CZ": 0},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Cestovné pro zahraniční porotce", "Jednotka": "cesta", "Cena za jednotku": 7000.0,
     "MP jednotky - MEZ": 18.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 18.0, "MP+TP jednotky - CZ": 0.0,
     "Cena MP - MEZ": 126000, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 0},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Překlady čeština/angličtina", "Jednotka": "strana textu", "Cena za jednotku": 500.0,
     "MP jednotky - MEZ": 450.0, "MP jednotky - CZ": 10.0, "MP+TP jednotky - MEZ": 700.0, "MP+TP jednotky - CZ": 10.0,
     "Cena MP - MEZ": 225000, "Cena MP - CZ": 5000, "Cena MP+TP - MEZ": 350000, "Cena MP+TP - CZ": 5000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Fotodokumentace celé soutěže (včetně zákresovách fotografií a dokumentace SW)", "Jednotka": "soubor", "Cena za jednotku": 65000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 65000, "Cena MP - CZ": 65000, "Cena MP+TP - MEZ": 65000, "Cena MP+TP - CZ": 65000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba vizuálního stylu grafickým studiem", "Jednotka": "soubor", "Cena za jednotku": 55000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 55000, "Cena MP - CZ": 55000, "Cena MP+TP - MEZ": 55000, "Cena MP+TP - CZ": 55000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba webu soutěže", "Jednotka": "soubor", "Cena za jednotku": 95000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 95000, "Cena MP - CZ": 95000, "Cena MP+TP - MEZ": 95000, "Cena MP+TP - CZ": 95000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafická úprava a sazba soutěžních podmínek a zadání", "Jednotka": "soubor", "Cena za jednotku": 35000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 35000, "Cena MP - CZ": 35000, "Cena MP+TP - MEZ": 35000, "Cena MP+TP - CZ": 35000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování katalogu", "Jednotka": "soubor", "Cena za jednotku": 50000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 50000, "Cena MP - CZ": 50000, "Cena MP+TP - MEZ": 50000, "Cena MP+TP - CZ": 50000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování výstavy", "Jednotka": "soubor", "Cena za jednotku": 70000.0,
     "MP jednotky - MEZ": 1.0, "MP jednotky - CZ": 1.0, "MP+TP jednotky - MEZ": 1.0, "MP+TP jednotky - CZ": 1.0,
     "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 70000, "Cena MP+TP - CZ": 70000},

    # Odměny
    {"Fáze": "Odměny", "Aktivita": "Odměny zahraničních porotců", "Jednotka": "odměna celková", "Cena za jednotku": 255000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 0.0,
     "Cena MP - MEZ": 765000, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 765000, "Cena MP+TP - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Odměny českých porotců", "Jednotka": "hod", "Cena za jednotku": 1800.0,
     "MP jednotky - MEZ": 192.0, "MP jednotky - CZ": 384.0, "MP+TP jednotky - MEZ": 192.0, "MP+TP jednotky - CZ": 384.0,
     "Cena MP - MEZ": 345600, "Cena MP - CZ": 691200, "Cena MP+TP - MEZ": 345600, "Cena MP+TP - CZ": 691200},
    
    {"Fáze": "Odměny", "Aktivita": "Odměny odborníků poroty", "Jednotka": "hod", "Cena za jednotku": 1800.0,
     "MP jednotky - MEZ": 192.0, "MP jednotky - CZ": 192.0, "MP+TP jednotky - MEZ": 256.0, "MP+TP jednotky - CZ": 256.0,
     "Cena MP - MEZ": 345600, "Cena MP - CZ": 345600, "Cena MP+TP - MEZ": 460800, "Cena MP+TP - CZ": 460800},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - mezinárodní soutěž", "Jednotka": "odměna pro tým", "Cena za jednotku": 1000000.0,
     "MP jednotky - MEZ": 5.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 5.0, "MP+TP jednotky - CZ": 0.0,
     "Cena MP - MEZ": 5000000, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 5000000, "Cena MP+TP - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - mezinárodní soutěž", "Jednotka": "odměna pro tým", "Cena za jednotku": 1000000.0,
     "MP jednotky - MEZ": 3.0, "MP jednotky - CZ": 0.0, "MP+TP jednotky - MEZ": 3.0, "MP+TP jednotky - CZ": 0.0,
     "Cena MP - MEZ": 3000000, "Cena MP - CZ": 0, "Cena MP+TP - MEZ": 3000000, "Cena MP+TP - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - soutěž v češtině", "Jednotka": "odměna pro tým", "Cena za jednotku": 750000.0,
     "MP jednotky - MEZ": 0.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 0.0, "MP+TP jednotky - CZ": 5.0,
     "Cena MP - MEZ": 0, "Cena MP - CZ": 3750000, "Cena MP+TP - MEZ": 0, "Cena MP+TP - CZ": 3750000},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - soutěž v češtině", "Jednotka": "odměna pro tým", "Cena za jednotku": 750000.0,
     "MP jednotky - MEZ": 0.0, "MP jednotky - CZ": 3.0, "MP+TP jednotky - MEZ": 0.0, "MP+TP jednotky - CZ": 3.0,
     "Cena MP - MEZ": 0, "Cena MP - CZ": 2250000, "Cena MP+TP - MEZ": 0, "Cena MP+TP - CZ": 2250000}
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
            
            jednotky = st.number_input(
                "Jednotek",
                min_value=0.0,
                value=float(jednotky_default),
                step=0.5,
                key=f"units_{faze}_{i}_{row['Aktivita'].replace(' ', '_')}_{jednotky_key}"
            )
            subtotal = jednotky * cena_za_jednotku
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Jednotka:** {row['Jednotka']}")
                st.write(f"**Cena za jednotku:** {cena_za_jednotku:,} Kč")
            with col2:
                st.write(f"**Subtotal:** {subtotal:,} Kč")
                st.write(f"**Původní cena:** {cena_za_aktivitu:,} Kč")
            
            if jednotky > 0:
                selected_activities.append({
                    "Fáze": faze,
                    "Aktivita": row['Aktivita'],
                    "Jednotka": row['Jednotka'],
                    "Množství": jednotky,
                    "Cena za jednotku": cena_za_jednotku,
                    "Subtotal": subtotal,
                    "Původní cena": cena_za_aktivitu
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
                elements.append(Paragr
