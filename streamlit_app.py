import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# --- Moderný dizajn inšpirovaný architektúrou a urbanizmom ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon=":building_construction:", layout="wide")

st.markdown("""
<style>
    /* Architektonické fonty a základné nastavenia */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        position: sticky;
        top: 0;
        z-index: 100;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 25%, #3498db 50%, #2980b9 75%, #1f4e79 100%);
        padding: 2rem;
        border-radius: 0;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border-bottom: 4px solid #e74c3c;
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
            linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.05) 10px, rgba(255,255,255,0.05) 20px);
        pointer-events: none;
    }
    
    .sticky-summary {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 25%, #3498db 50%, #2980b9 75%, #1f4e79 100%);
        color: white;
        text-align: center;
        padding: 1.5rem 0.5rem 1rem 0.5rem;
        z-index: 9999;
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        box-shadow: 0 -8px 32px rgba(0,0,0,0.2);
        border-top: 4px solid #e74c3c;
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ecf0f1 0%, #bdc3c7 100%);
        padding: 2rem;
        border-radius: 0;
        color: #2c3e50;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-left: 6px solid #3498db;
        font-family: 'Inter', sans-serif;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
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
        background: linear-gradient(90deg, #3498db, #e74c3c, #f39c12, #27ae60);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }
    
    .phase-header {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1.5rem 2rem;
        border-radius: 0;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        border-left: 8px solid #e74c3c;
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
        border-width: 0 0 50px 50px;
        border-color: transparent transparent #e74c3c transparent;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 0;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        border-bottom: 4px solid #3498db;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 0;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 2px solid #dee2e6;
        position: relative;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3498db, #e74c3c, #f39c12, #27ae60);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        border: none;
        border-radius: 0;
        padding: 1rem 2.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        border-bottom: 4px solid #e74c3c;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #3498db 0%, #e74c3c 25%, #f39c12 50%, #27ae60 75%, #9b59b6 100%);
        height: 8px;
        border-radius: 0;
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
    
    /* Urbanistické mriežky */
    .grid-pattern {
        background-image: 
            linear-gradient(rgba(52, 152, 219, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(52, 152, 219, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Architektonické stĺpce */
    .column-architectural {
        background: linear-gradient(180deg, #ecf0f1 0%, #bdc3c7 100%);
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 0.5rem 0;
        position: relative;
    }
    
    .column-architectural::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #3498db, #e74c3c);
    }
    
    /* Moderné karty s architektonickými prvkami */
    .architectural-card {
        background: white;
        border-radius: 0;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 2px solid #dee2e6;
        position: relative;
        overflow: hidden;
    }
    
    .architectural-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #3498db, #e74c3c, #f39c12, #27ae60);
    }
    
    /* Urbanistické ikony a prvky */
    .urban-icon {
        display: inline-block;
        width: 20px;
        height: 20px;
        background: linear-gradient(45deg, #3498db, #e74c3c);
        margin-right: 8px;
        border-radius: 2px;
    }
    
    /* Responsívny dizajn */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.2rem;
            padding: 1.5rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <div style="font-size: 0.9rem; opacity: 0.9; margin-top: 1rem;">
        <span class="urban-icon"></span>Urbanistické riešenia
        <span class="urban-icon"></span>Architektonické inovácie
        <span class="urban-icon"></span>Mestské plánovanie
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar s architektonickým dizajnom ---
st.sidebar.markdown("""
<div class="sidebar-header">
    <h3>Nastavenia projektu</h3>
</div>
""", unsafe_allow_html=True)

variant = st.sidebar.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    help="Zvoľte typ soutěže."
)
unit_type = st.sidebar.radio(
    "Vyberte typ jednotek:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
    help="Vyberte, či chcete počítať len MP alebo aj transformačné plochy."
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

# --- DataFrame ---
df = pd.DataFrame(activities_data)
df = df.fillna(0)
df["Poznámka"] = ""
df["Vybrané"] = True  # Predvolene všetky aktivity vybrané

# --- Filtrovanie podľa fázy ---
fazes = df["Fáze"].unique().tolist()
selected_fazes = st.sidebar.multiselect(
    "Filtrovať fázy:", fazes, default=fazes, help="Vyberte, ktoré fázy chcete zobraziť."
)

# --- Reset ---
if st.sidebar.button("Resetovať všetky hodnoty na default"):
    st.session_state.clear()
    st.experimental_rerun()

# --- Výber kľúčov podľa variantu a jednotiek ---
vkey = "MEZ" if "Mezinárodní" in variant else "CZ"
ukey = "MP" if "MP)" in unit_type else "MP+TP"
jednotky_key = f"{ukey} jednotky - {vkey}"
cena_key = f"Cena za jednotku"

# --- Príprava editovateľnej tabuľky ---
df_filtered = df[df["Fáze"].isin(selected_fazes)].copy()
df_filtered["Množství"] = df_filtered[jednotky_key]
df_filtered["Cena za jednotku"] = df_filtered[cena_key]
df_filtered["Subtotal"] = df_filtered["Množství"] * df_filtered["Cena za jednotku"]

# --- Interaktívna tabuľka s architektonickým dizajnom ---
st.markdown("""
<div class="architectural-card">
    <h3>Detailní přehled aktivit</h3>
</div>
""", unsafe_allow_html=True)

edited_df = st.data_editor(
    df_filtered[["Vybrané", "Fáze", "Aktivita", "Jednotka", "Množství", "Cena za jednotku", "Subtotal", "Poznámka"]],
    column_config={
        "Vybrané": st.column_config.CheckboxColumn("Vybrané", help="Zahrnúť aktivitu do výpočtu."),
        "Množství": st.column_config.NumberColumn("Množství", min_value=0, step=0.5, help="Zadajte počet jednotiek."),
        "Cena za jednotku": st.column_config.NumberColumn("Cena za jednotku", min_value=0, step=100, help="Zadajte cenu za jednotku."),
        "Poznámka": st.column_config.TextColumn("Poznámka", help="Vaša poznámka k aktivite.")
    },
    use_container_width=True,
    num_rows="dynamic",
    key="main_table"
)
edited_df["Subtotal"] = edited_df["Množství"] * edited_df["Cena za jednotku"]

# --- Filter len vybrané aktivity ---
selected_df = edited_df[edited_df["Vybrané"] == True].copy()

# --- Rýchle sumáre ---
total = selected_df["Subtotal"].sum()
vat_amount = total * 0.21
total_with_vat = total * 1.21

# --- Sticky sumár dole ---
st.markdown(f"""
<div class="sticky-summary">
    <b>Celková suma bez DPH:</b> {total:,.0f} Kč &nbsp; | &nbsp;
    <b>DPH (21%):</b> {vat_amount:,.0f} Kč &nbsp; | &nbsp;
    <b>Celková suma s DPH:</b> {total_with_vat:,.0f} Kč
</div>
""", unsafe_allow_html=True)

# --- Moderné grafy s architektonickým dizajnom ---
st.markdown("---")
st.markdown("""
<div class="architectural-card">
    <h3>Vizualizace nákladů (len vybrané aktivity)</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig_sunburst = px.sunburst(
        selected_df,
        path=['Fáze', 'Aktivita'],
        values='Subtotal',
        color='Fáze',
        color_discrete_sequence=['#2c3e50', '#34495e', '#3498db', '#2980b9', '#1f4e79', '#e74c3c', '#f39c12'],
        title='Hierarchické rozloženie nákladov',
        hover_data={'Subtotal':':,.0f', 'Množství':True, 'Cena za jednotku':True, 'Poznámka':True}
    )
    fig_sunburst.update_traces(insidetextorientation='radial')
    fig_sunburst.update_layout(
        font=dict(family="Inter", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)
with col2:
    fig_bar = px.bar(
        selected_df,
        x='Aktivita',
        y='Subtotal',
        title='Náklady podľa aktivít',
        color='Fáze',
        color_discrete_sequence=['#2c3e50', '#34495e', '#3498db', '#2980b9', '#1f4e79', '#e74c3c', '#f39c12'],
        hover_data={'Subtotal':':,.0f', 'Množství':True, 'Cena za jednotku':True, 'Poznámka':True}
    )
    fig_bar.update_xaxes(tickangle=45)
    fig_bar.update_layout(
        font=dict(family="Inter", size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Export s architektonickým dizajnom ---
st.markdown("---")
st.markdown("""
<div class="architectural-card">
    <h3>Export výsledků (len vybrané aktivity)</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    excel_buffer = BytesIO()
    selected_df.to_excel(excel_buffer, index=False)
    st.download_button(
        label="Stáhnout Excel",
        data=excel_buffer.getvalue(),
        file_name="soutezni_workshop_rozpocet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    st.info("Export do PDF bude čoskoro dostupný v ďalšej verzii.")

# --- Footer s architektonickým dizajnom ---
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #2c3e50; padding: 2rem; font-family: "Inter", sans-serif;'>
    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
        Kalkulátor soutěžního workshopu
    </div>
    <div style="font-size: 0.9rem; opacity: 0.7;">
        Urbanistické riešenia | Architektonické inovácie | Mestské plánovanie
    </div>
    <div style="font-size: 0.8rem; opacity: 0.5; margin-top: 0.5rem;">
        {datetime.now().strftime('%d.%m.%Y %H:%M')}
    </div>
</div>
""", unsafe_allow_html=True)
