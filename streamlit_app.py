import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# --- Dizajn inšpirovaný 4ct.eu ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
    /* 4ct.eu inšpirovaný dizajn */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Základné nastavenia */
    .main {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hlavička v štýle 4ct.eu */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        padding: 3rem 2rem;
        margin: -2rem -2rem 2rem -2rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%),
            linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.05) 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 1rem 0 0 0;
        font-weight: 400;
    }
    
    /* 4ct.eu logo štýl */
    .brand-logo {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar v štýle 4ct.eu */
    .sidebar-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
    }
    
    /* Karty v štýle 4ct.eu */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        color: #1f2937;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #1e3a8a);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Fázy v štýle 4ct.eu */
    .phase-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
        position: relative;
    }
    
    .phase-header::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 0;
        height: 0;
        border-style: solid;
        border-width: 0 0 40px 40px;
        border-color: transparent transparent rgba(255,255,255,0.2) transparent;
    }
    
    /* Grafy v štýle 4ct.eu */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        position: relative;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #1e3a8a);
    }
    
    /* Tlačidlá v štýle 4ct.eu */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
        text-transform: none;
        letter-spacing: 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.3);
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
    }
    
    /* Progress bar v štýle 4ct.eu */
    .progress-bar {
        background: linear-gradient(90deg, #3b82f6 0%, #1e3a8a 100%);
        height: 6px;
        border-radius: 3px;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Sticky summary v štýle 4ct.eu */
    .sticky-summary {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        text-align: center;
        padding: 1.5rem 0.5rem 1rem 0.5rem;
        z-index: 9999;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 -4px 20px rgba(59, 130, 246, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Tabuľka v štýle 4ct.eu */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        font-weight: 600;
        padding: 1rem;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* Checkbox štýl */
    .stCheckbox > label {
        font-weight: 500;
        color: #1f2937;
    }
    
    /* Radio buttons štýl */
    .stRadio > label {
        font-weight: 500;
        color: #1f2937;
    }
    
    /* Responsívny dizajn */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
    }
    
    /* 4ct.eu geometrické prvky */
    .geometric-pattern {
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: 
            linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%),
            linear-gradient(-45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <div class="brand-logo">4CT Platform</div>
    <div class="geometric-pattern"></div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar s 4ct.eu dizajnom ---
st.sidebar.markdown("""
<div class="sidebar-header">
    <h3>Nastavení projektu</h3>
</div>
""", unsafe_allow_html=True)

variant = st.sidebar.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    help="Vyberte typ soutěže."
)
unit_type = st.sidebar.radio(
    "Vyberte typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
    help="Vyberte, zda chcete počítat pouze MP nebo i transformační plochy."
)

# --- Dáta ---
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
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Komunikace s médii a veřejností", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 8.0, "MP jednotky - CZ": 6.0, "MP+TP jednotky - MEZ": 8.0, "MP+TP jednotky - CZ": 6.0,
     "Cena MP - MEZ": 112000, "Cena MP - CZ": 84000, "Cena MP+TP - MEZ": 112000, "Cena MP+TP - CZ": 84000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Organizace veřejných prezentací a diskuzí", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 12.0, "MP jednotky - CZ": 10.0, "MP+TP jednotky - MEZ": 12.0, "MP+TP jednotky - CZ": 10.0,
     "Cena MP - MEZ": 168000, "Cena MP - CZ": 140000, "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 140000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Zpracování a distribuce tiskových materiálů", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "MP jednotky - MEZ": 6.0, "MP jednotky - CZ": 5.0, "MP+TP jednotky - MEZ": 6.0, "MP+TP jednotky - CZ": 5.0,
     "Cena MP - MEZ": 84000, "Cena MP - CZ": 70000, "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 70000}
]

# --- Vytvoření DataFrame ---
df = pd.DataFrame(activities_data)

# --- Výpočet hodnot na základě výběru ---
if variant == "Mezinárodní soutěžní workshop":
    variant_suffix = "MEZ"
else:
    variant_suffix = "CZ"

if unit_type == "Počet jednotek (změna MP)":
    unit_col = f"MP jednotky - {variant_suffix}"
    price_col = f"Cena MP - {variant_suffix}"
else:
    unit_col = f"MP+TP jednotky - {variant_suffix}"
    price_col = f"Cena MP+TP - {variant_suffix}"

# --- Přidání sloupců pro editaci ---
df['Vybrané'] = True
df['Upravené množství'] = df[unit_col]
df['Upravená cena za jednotku'] = df['Cena za jednotku']
df['Poznámky'] = ''

# --- Filtrování fází ---
phases = df['Fáze'].unique()
selected_phases = st.sidebar.multiselect(
    "Filtrujte fáze:",
    phases,
    default=phases,
    help="Vyberte fáze, které chcete zobrazit."
)

# --- Filtrování dat ---
filtered_df = df[df['Fáze'].isin(selected_phases)].copy()

# --- Hlavní obsah ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>Celkové náklady</h3>
        <h2 style="color: #1e3a8a; margin: 0;">{total_cost:,.0f} Kč</h2>
        <p style="margin: 0; opacity: 0.7;">Celková suma</p>
    </div>
    """.format(total_cost=filtered_df[price_col].sum()), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>Počet aktivit</h3>
        <h2 style="color: #1e3a8a; margin: 0;">{activity_count}</h2>
        <p style="margin: 0; opacity: 0.7;">Celkový počet</p>
    </div>
    """.format(activity_count=len(filtered_df)), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Průměrná cena</h3>
        <h2 style="color: #1e3a8a; margin: 0;">{avg_cost:,.0f} Kč</h2>
        <p style="margin: 0; opacity: 0.7;">Na aktivitu</p>
    </div>
    """.format(avg_cost=filtered_df[price_col].mean()), unsafe_allow_html=True)

# --- Progress bar ---
st.markdown("""
<div class="progress-bar"></div>
""", unsafe_allow_html=True)

# --- Interaktivní tabulka ---
st.markdown("""
<div class="phase-header">
    <h3>Interaktivní tabulka aktivit</h3>
</div>
""", unsafe_allow_html=True)

# Vytvoření editovatelné tabulky
edited_df = st.data_editor(
    filtered_df[['Vybrané', 'Fáze', 'Aktivita', 'Upravené množství', 'Upravená cena za jednotku', 'Poznámky']],
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Vybrané": st.column_config.CheckboxColumn("Vybrané", help="Označte aktivitu jako vybranou"),
        "Fáze": st.column_config.TextColumn("Fáze", disabled=True),
        "Aktivita": st.column_config.TextColumn("Aktivita", disabled=True),
        "Upravené množství": st.column_config.NumberColumn("Množství", min_value=0.0, step=0.5),
        "Upravená cena za jednotku": st.column_config.NumberColumn("Cena za jednotku (Kč)", min_value=0.0, step=1000.0),
        "Poznámky": st.column_config.TextColumn("Poznámky", max_chars=200)
    }
)

# --- Výpočet upravených hodnot ---
selected_activities = edited_df[edited_df['Vybrané'] == True]
total_selected_cost = (selected_activities['Upravené množství'] * selected_activities['Upravená cena za jednotku']).sum()

# --- Grafy ---
st.markdown("""
<div class="chart-container">
    <h3 style="text-align: center; color: #1e3a8a; margin-bottom: 2rem;">Vizualizace nákladů</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Sunburst chart pro fáze
    phase_costs = selected_activities.groupby('Fáze')['Upravené množství'].sum()
    fig_sunburst = px.sunburst(
        names=phase_costs.index,
        parents=[''] * len(phase_costs),
        values=phase_costs.values,
        title="Rozložení nákladů podle fází",
        color_discrete_sequence=['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe']
    )
    fig_sunburst.update_layout(
        title_x=0.5,
        title_font_size=16,
        title_font_color='#1e3a8a'
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)

with col2:
    # Bar chart pro top aktivity
    top_activities = selected_activities.nlargest(10, 'Upravené množství')
    fig_bar = px.bar(
        top_activities,
        x='Aktivita',
        y='Upravené množství',
        title="Top 10 nejnáročnějších aktivit",
        color_discrete_sequence=['#3b82f6']
    )
    fig_bar.update_layout(
        title_x=0.5,
        title_font_size=16,
        title_font_color='#1e3a8a',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Export ---
st.markdown("""
<div class="phase-header">
    <h3>Export dat</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Export do Excel", type="primary"):
        # Vytvoření Excel souboru
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            selected_activities.to_excel(writer, sheet_name='Vybrané aktivity', index=False)
            
            # Přidání shrnutí
            summary_data = {
                'Metrika': ['Celkové náklady', 'Počet aktivit', 'Průměrná cena na aktivitu'],
                'Hodnota': [
                    f"{total_selected_cost:,.0f} Kč",
                    len(selected_activities),
                    f"{total_selected_cost/len(selected_activities):,.0f} Kč"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Shrnutí', index=False)
        
        output.seek(0)
        st.download_button(
            label="Stáhnout Excel soubor",
            data=output.getvalue(),
            file_name=f"kalkulace_soutezniho_workshopu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col2:
    if st.button("Reset hodnot"):
        st.rerun()

# --- Sticky summary ---
st.markdown(f"""
<div class="sticky-summary">
    Celkové náklady: {total_selected_cost:,.0f} Kč | Vybrané aktivity: {len(selected_activities)} | Průměrná cena: {total_selected_cost/len(selected_activities):,.0f} Kč
</div>
""", unsafe_allow_html=True)
