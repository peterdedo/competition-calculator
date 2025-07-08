import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO

# --- Najmodernejší vizuál a UX podľa svetových štandardov ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    html, body, .main { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important; font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 40%, #60a5fa 100%);
        padding: 4rem 2rem 2.5rem 2rem;
        margin: -2rem -2rem 2.5rem -2rem;
        color: white;
        text-align: center;
        border-radius: 0 0 2.5rem 2.5rem;
        box-shadow: 0 12px 48px rgba(30,58,138,0.18);
        position: relative;
        overflow: hidden;
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        text-shadow: 0 2px 16px rgba(30,58,138,0.12);
    }
    .main-header p {
        font-size: 1.25rem;
        font-weight: 400;
        opacity: 0.95;
        margin-bottom: 0.5rem;
    }
    .main-header .brand-logo {
        display: inline-block;
        background: rgba(255,255,255,0.13);
        padding: 0.5rem 1.5rem;
        border-radius: 1rem;
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 1.5rem;
        letter-spacing: 0.08em;
        box-shadow: 0 2px 12px rgba(30,58,138,0.08);
    }
    .main-header .hero-bg {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('data:image/svg+xml;utf8,<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><rect fill="none"/><circle cx="80" cy="80" r="60" fill="%233b82f6" fill-opacity="0.08"/><circle cx="90%" cy="30" r="80" fill="%231e3a8a" fill-opacity="0.06"/><rect x="60%" y="60%" width="120" height="120" rx="30" fill="%2360a5fa" fill-opacity="0.07"/></svg>');
        z-index: 0;
        pointer-events: none;
    }
    .sidebar-header {
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 1.5rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 4px 24px rgba(30,58,138,0.10);
        position: sticky;
        top: 1.5rem;
        z-index: 10;
    }
    .stRadio, .stMultiSelect, .stButton, .stCheckbox {
        font-size: 1.1rem !important;
    }
    .metric-card {
        background: linear-gradient(120deg, #fff 60%, #e0e7ef 100%);
        padding: 2.2rem 1.5rem 1.5rem 1.5rem;
        border-radius: 1.5rem;
        color: #1e2937;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 24px rgba(30,58,138,0.08);
        border: 1.5px solid #e5e7eb;
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .metric-card:hover {
        box-shadow: 0 8px 32px rgba(30,58,138,0.16);
        transform: translateY(-2px) scale(1.01);
    }
    .metric-card h3 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.2rem;
    }
    .metric-card h2 {
        font-size: 2.2rem;
        font-weight: 900;
        color: #1e3a8a;
        margin: 0.2rem 0 0.1rem 0;
        letter-spacing: -0.02em;
    }
    .metric-card p {
        font-size: 1rem;
        opacity: 0.7;
        margin: 0;
    }
    .phase-header {
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem 2rem;
        border-radius: 1.2rem;
        color: white;
        margin: 2rem 0 1.2rem 0;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 20px rgba(30,58,138,0.10);
        border-left: 8px solid #60a5fa;
        position: relative;
    }
    .chart-container {
        background: linear-gradient(120deg, #fff 60%, #e0e7ef 100%);
        border-radius: 1.5rem;
        padding: 2.5rem 2rem 2rem 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 24px rgba(30,58,138,0.08);
        border: 1.5px solid #e5e7eb;
        position: relative;
    }
    .stButton > button {
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 1rem;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 20px rgba(30,58,138,0.10);
        text-transform: none;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 8px 32px rgba(30,58,138,0.18);
        background: linear-gradient(120deg, #2563eb 0%, #60a5fa 100%);
    }
    .progress-bar {
        background: linear-gradient(90deg, #3b82f6 0%, #1e3a8a 100%);
        height: 8px;
        border-radius: 4px;
        margin: 2rem 0 1.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(30,58,138,0.10);
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
    .sticky-summary {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        text-align: center;
        padding: 1.2rem 0.5rem 1rem 0.5rem;
        z-index: 9999;
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: 0 -4px 24px rgba(30,58,138,0.12);
        border-top-left-radius: 1.5rem;
        border-top-right-radius: 1.5rem;
        letter-spacing: 0.02em;
        backdrop-filter: blur(10px);
    }
    .dataframe {
        border-radius: 1.2rem;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(30,58,138,0.08);
        border: 1.5px solid #e5e7eb;
    }
    .dataframe th {
        background: linear-gradient(120deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        font-weight: 700;
        padding: 1rem;
        font-size: 1.1rem;
    }
    .dataframe td {
        padding: 0.85rem;
        border-bottom: 1px solid #e5e7eb;
        font-size: 1.05rem;
    }
    .stCheckbox > label, .stRadio > label {
        font-weight: 600;
        color: #1e2937;
    }
    @media (max-width: 900px) {
        .main-header h1 { font-size: 2.1rem; }
        .main-header p { font-size: 1rem; }
        .metric-card { padding: 1.2rem; }
        .chart-container { padding: 1.2rem; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="hero-bg"></div>
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <div class="brand-logo">4CT Platform</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("""
<div class="sidebar-header">
    <span style="font-size:1.5rem;vertical-align:middle;">⚙️</span> Nastavení projektu
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

# --- KPI cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Celkové náklady</h3>
        <h2>{filtered_df[price_col].sum():,.0f} Kč</h2>
        <p>Celková suma</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Počet aktivit</h3>
        <h2>{len(filtered_df)}</h2>
        <p>Celkový počet</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Průměrná cena</h3>
        <h2>{filtered_df[price_col].mean():,.0f} Kč</h2>
        <p>Na aktivitu</p>
    </div>
    """, unsafe_allow_html=True)

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
    selected_activities['Náklady'] = selected_activities['Upravené množství'] * selected_activities['Upravená cena za jednotku']
    phase_costs = selected_activities.groupby('Fáze')['Náklady'].sum()
    fig_sunburst = px.sunburst(
        names=phase_costs.index,
        parents=[''] * len(phase_costs),
        values=phase_costs.values,
        title="Rozložení nákladů podle fází",
        color_discrete_sequence=[
            'rgba(30,58,138,0.95)', 'rgba(59,130,246,0.85)', 'rgba(96,165,250,0.8)', 'rgba(147,197,253,0.7)', 'rgba(219,234,254,0.6)'
        ]
    )
    fig_sunburst.update_layout(
        title_x=0.5,
        title_font_size=20,
        title_font_color='#1e3a8a',
        height=520,
        margin=dict(t=60, l=0, r=0, b=0),
        paper_bgcolor='rgba(255,255,255,0.95)',
        font=dict(family='Inter, sans-serif', size=16, color='#1e2937'),
        sunburstcolorway=[
            '#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'
        ]
    )
    fig_sunburst.update_traces(
        hovertemplate='<b>%{label}</b><br>Celkové náklady: %{value:,.0f} Kč<extra></extra>',
        marker=dict(line=dict(width=2, color='white')),
        insidetextorientation='radial',
        textfont_size=18
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)
with col2:
    top_activities = selected_activities.nlargest(10, 'Náklady')
    fig_bar = px.bar(
        top_activities,
        x='Aktivita',
        y='Náklady',
        title="Top 10 nejnáročnějších aktivit podle nákladů",
        color='Náklady',
        color_continuous_scale=[
            '#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'
        ],
        text=top_activities['Náklady'].apply(lambda x: f'{x:,.0f} Kč')
    )
    fig_bar.update_layout(
        title_x=0.5,
        title_font_size=20,
        title_font_color='#1e3a8a',
        xaxis_tickangle=-30,
        height=520,
        margin=dict(t=60, l=0, r=0, b=0),
        paper_bgcolor='rgba(255,255,255,0.95)',
        font=dict(family='Inter, sans-serif', size=16, color='#1e2937'),
        plot_bgcolor='rgba(240,245,255,0.7)',
        showlegend=False
    )
    fig_bar.update_traces(
        textposition='outside',
        marker_line_width=2,
        marker_line_color='#fff',
        hovertemplate='<b>%{x}</b><br>Celkové náklady: %{y:,.0f} Kč<extra></extra>'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Dodatočné grafy ---
st.markdown("""
<div class="chart-container">
    <h3 style="text-align: center; color: #1e3a8a; margin-bottom: 2rem;">Detailní analýza</h3>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    fig_pie = px.pie(
        values=phase_costs.values,
        names=phase_costs.index,
        title="Procentuální rozložení nákladů",
        color_discrete_sequence=[
            '#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'
        ]
    )
    fig_pie.update_layout(
        title_x=0.5,
        title_font_size=18,
        title_font_color='#1e3a8a',
        height=400,
        margin=dict(t=60, l=0, r=0, b=0),
        paper_bgcolor='rgba(255,255,255,0.95)',
        font=dict(family='Inter, sans-serif', size=16, color='#1e2937')
    )
    fig_pie.update_traces(
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Celkové náklady: %{value:,.0f} Kč<br>Podíl: %{percent}<extra></extra>',
        marker=dict(line=dict(width=2, color='white')),
        pull=[0.05]*len(phase_costs)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
with col2:
    phase_order = ['Analytická fáze', 'Přípravní fáze', 'Průběh soutěžního workshopu (SW)', 
                   'Vyhlášení výsledků SW', 'PR podpora v průběhu celé soutěže']
    phase_costs_ordered = phase_costs.reindex([p for p in phase_order if p in phase_costs.index])
    fig_line = px.line(
        x=phase_costs_ordered.index,
        y=phase_costs_ordered.values,
        title="Trend nákladů podle fází",
        markers=True
    )
    fig_line.update_layout(
        title_x=0.5,
        title_font_size=18,
        title_font_color='#1e3a8a',
        xaxis_title="Fáze",
        yaxis_title="Náklady (Kč)",
        height=400,
        margin=dict(t=60, l=0, r=0, b=0),
        paper_bgcolor='rgba(255,255,255,0.95)',
        font=dict(family='Inter, sans-serif', size=16, color='#1e2937'),
        plot_bgcolor='rgba(240,245,255,0.7)'
    )
    fig_line.update_traces(
        line_color='#3b82f6',
        marker_color='#1e3a8a',
        marker_size=12,
        marker_line_width=2,
        marker_line_color='#fff',
        hovertemplate='<b>%{x}</b><br>Celkové náklady: %{y:,.0f} Kč<extra></extra>'
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- Export ---
st.markdown("""
<div class="phase-header">
    <h3>Export dat</h3>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("Export do Excel", type="primary"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            selected_activities.to_excel(writer, sheet_name='Vybrané aktivity', index=False)
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
