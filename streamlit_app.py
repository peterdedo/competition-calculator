import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

# --- Najmodernejší vizuál a UX podľa svetových štandardov ---
st.set_page_config(page_title="Kalkulátor soutěžního workshopu", page_icon="🏗️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    html, body, .main { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important; font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(120deg, #059669 0%, #10b981 40%, #34d399 100%);
        padding: 4rem 2rem 2.5rem 2rem;
        margin: -2rem -2rem 2.5rem -2rem;
        color: white;
        text-align: center;
        border-radius: 0 0 2.5rem 2.5rem;
        box-shadow: 0 12px 48px rgba(5,150,105,0.18);
        position: relative;
        overflow: hidden;
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        text-shadow: 0 2px 16px rgba(5,150,105,0.12);
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
        box-shadow: 0 2px 12px rgba(5,150,105,0.08);
    }
    .main-header .hero-bg {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url('data:image/svg+xml;utf8,<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><rect fill="none"/><circle cx="80" cy="80" r="60" fill="%2310b981" fill-opacity="0.08"/><circle cx="90%" cy="30" r="80" fill="%23059669" fill-opacity="0.06"/><rect x="60%" y="60%" width="120" height="120" rx="30" fill="%2334d399" fill-opacity="0.07"/></svg>');
        z-index: 0;
        pointer-events: none;
    }
    .sidebar-header {
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
        padding: 2rem 1rem 1.5rem 1rem;
        border-radius: 1.5rem;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 4px 24px rgba(5,150,105,0.10);
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
        box-shadow: 0 4px 24px rgba(5,150,105,0.08);
        border: 1.5px solid #e5e7eb;
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .metric-card:hover {
        box-shadow: 0 8px 32px rgba(5,150,105,0.16);
        transform: translateY(-2px) scale(1.01);
    }
    .metric-card h3 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 0.2rem;
    }
    .metric-card h2 {
        font-size: 2.2rem;
        font-weight: 900;
        color: #059669;
        margin: 0.2rem 0 0.1rem 0;
        letter-spacing: -0.02em;
    }
    .metric-card p {
        font-size: 1rem;
        opacity: 0.7;
        margin: 0;
    }
    .phase-header {
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
        padding: 1.5rem 2rem;
        border-radius: 1.2rem;
        color: white;
        margin: 2rem 0 1.2rem 0;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 4px 20px rgba(5,150,105,0.10);
        border-left: 8px solid #34d399;
        position: relative;
    }
    .chart-container {
        background: linear-gradient(120deg, #fff 60%, #e0e7ef 100%);
        border-radius: 1.5rem;
        padding: 2.5rem 2rem 2rem 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 24px rgba(5,150,105,0.08);
        border: 1.5px solid #e5e7eb;
        position: relative;
    }
    .stButton > button {
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
        color: white;
        border: none;
        border-radius: 1rem;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 20px rgba(5,150,105,0.10);
        text-transform: none;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 8px 32px rgba(5,150,105,0.18);
        background: linear-gradient(120deg, #047857 0%, #34d399 100%);
    }
    .progress-bar {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        height: 8px;
        border-radius: 4px;
        margin: 2rem 0 1.5rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(5,150,105,0.10);
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
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
        color: white;
        text-align: center;
        padding: 1.2rem 0.5rem 1rem 0.5rem;
        z-index: 9999;
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: 0 -4px 24px rgba(5,150,105,0.12);
        border-top-left-radius: 1.5rem;
        border-top-right-radius: 1.5rem;
        letter-spacing: 0.02em;
        backdrop-filter: blur(10px);
    }
    .dataframe {
        border-radius: 1.2rem;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(5,150,105,0.08);
        border: 1.5px solid #e5e7eb;
    }
    .dataframe th {
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
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
    <div class="brand-logo">4ct platform</div>
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
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 2.0, "Cena (MP) - EN": 14000, "Cena (MP+T) - EN": 28000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 2.0, "Cena (MP) - CZ": 14000, "Cena (MP+T) - CZ": 28000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Vymezení řešeného území", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 2.0, "Cena (MP) - EN": 14000, "Cena (MP+T) - EN": 28000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 2.0, "Cena (MP) - CZ": 14000, "Cena (MP+T) - CZ": 28000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Seznámení se s dostupnými materiály a záměry v území", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 6.0, "Počet MJ (MP+T) - EN": 8.0, "Cena (MP) - EN": 84000, "Cena (MP+T) - EN": 112000,
     "Počet MJ (MP) - CZ": 6.0, "Počet MJ (MP+T) - CZ": 8.0, "Cena (MP) - CZ": 84000, "Cena (MP+T) - CZ": 112000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Analýza stavu území na základě předem definovaných parametrů a indikátorů", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 32.0, "Počet MJ (MP+T) - EN": 42.0, "Cena (MP) - EN": 448000, "Cena (MP+T) - EN": 588000,
     "Počet MJ (MP) - CZ": 32.0, "Počet MJ (MP+T) - CZ": 42.0, "Cena (MP) - CZ": 448000, "Cena (MP+T) - CZ": 588000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 8.0, "Počet MJ (MP+T) - EN": 11.0, "Cena (MP) - EN": 112000, "Cena (MP+T) - EN": 154000,
     "Počet MJ (MP) - CZ": 8.0, "Počet MJ (MP+T) - CZ": 11.0, "Cena (MP) - CZ": 112000, "Cena (MP+T) - CZ": 154000},
    
    {"Fáze": "Analytická fáze", "Aktivita": "Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 6.0, "Cena (MP) - EN": 42000, "Cena (MP+T) - EN": 84000,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 6.0, "Cena (MP) - CZ": 42000, "Cena (MP+T) - CZ": 84000},

    # Přípravní fáze
    {"Fáze": "Přípravní fáze", "Aktivita": "Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 15.0, "Počet MJ (MP+T) - EN": 20.0, "Cena (MP) - EN": 210000, "Cena (MP+T) - EN": 280000,
     "Počet MJ (MP) - CZ": 15.0, "Počet MJ (MP+T) - CZ": 20.0, "Cena (MP) - CZ": 210000, "Cena (MP+T) - CZ": 280000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení podrobného rozpočtu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 4.0, "Cena (MP) - EN": 42000, "Cena (MP+T) - EN": 56000,
     "Počet MJ (MP) - CZ": 2.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 28000, "Cena (MP+T) - CZ": 42000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 10.0, "Počet MJ (MP+T) - EN": 15.0, "Cena (MP) - EN": 140000, "Cena (MP+T) - EN": 210000,
     "Počet MJ (MP) - CZ": 10.0, "Počet MJ (MP+T) - CZ": 15.0, "Cena (MP) - CZ": 140000, "Cena (MP+T) - CZ": 210000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 0.0, "Počet MJ (MP+T) - EN": 15.0, "Cena (MP) - EN": 0, "Cena (MP+T) - EN": 210000,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 15.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 210000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Vytvoření značky soutěže (včetně konzultace se zadavatelem)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 4.0, "Počet MJ (MP+T) - EN": 4.0, "Cena (MP) - EN": 56000, "Cena (MP+T) - EN": 56000,
     "Počet MJ (MP) - CZ": 4.0, "Počet MJ (MP+T) - CZ": 4.0, "Cena (MP) - CZ": 56000, "Cena (MP+T) - CZ": 56000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "PR strategie projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 4.0, "Počet MJ (MP+T) - EN": 4.0, "Cena (MP) - EN": 56000, "Cena (MP+T) - EN": 56000,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 42000, "Cena (MP+T) - CZ": 42000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace zadání (parametry využití území, stavební program, průběžná jednání s ŘS a PS)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 30.0, "Počet MJ (MP+T) - EN": 50.0, "Cena (MP) - EN": 420000, "Cena (MP+T) - EN": 700000,
     "Počet MJ (MP) - CZ": 25.0, "Počet MJ (MP+T) - CZ": 40.0, "Cena (MP) - CZ": 350000, "Cena (MP+T) - CZ": 560000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Formulace soutěžních podmínek", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 16.0, "Počet MJ (MP+T) - EN": 20.0, "Cena (MP) - EN": 224000, "Cena (MP+T) - EN": 280000,
     "Počet MJ (MP) - CZ": 16.0, "Počet MJ (MP+T) - CZ": 20.0, "Cena (MP) - CZ": 224000, "Cena (MP+T) - CZ": 280000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Finalizace a publikace soutěžních podmínek a zadání", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 4.0, "Počet MJ (MP+T) - EN": 5.0, "Cena (MP) - EN": 56000, "Cena (MP+T) - EN": 70000,
     "Počet MJ (MP) - CZ": 4.0, "Počet MJ (MP+T) - CZ": 5.0, "Cena (MP) - CZ": 56000, "Cena (MP+T) - CZ": 70000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení poroty", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 6.0, "Počet MJ (MP+T) - EN": 9.0, "Cena (MP) - EN": 84000, "Cena (MP+T) - EN": 126000,
     "Počet MJ (MP) - CZ": 5.0, "Počet MJ (MP+T) - CZ": 8.0, "Cena (MP) - CZ": 70000, "Cena (MP+T) - CZ": 112000},
    
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace před vyhlášením soutěže a ustavující schůze poroty (včetně regulérnosti ČKA)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 23.0, "Počet MJ (MP+T) - EN": 25.0, "Cena (MP) - EN": 322000, "Cena (MP+T) - EN": 350000,
     "Počet MJ (MP) - CZ": 23.0, "Počet MJ (MP+T) - CZ": 25.0, "Cena (MP) - CZ": 322000, "Cena (MP+T) - CZ": 350000},

    # Průběh soutěžního workshopu (SW)
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Vyhlášení soutěže – otevřená výzva a výběr soutěžících", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 7.0, "Počet MJ (MP+T) - EN": 7.0, "Cena (MP) - EN": 98000, "Cena (MP+T) - EN": 98000,
     "Počet MJ (MP) - CZ": 5.0, "Počet MJ (MP+T) - CZ": 5.0, "Cena (MP) - CZ": 70000, "Cena (MP+T) - CZ": 70000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 1. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 30.0, "Počet MJ (MP+T) - EN": 30.0, "Cena (MP) - EN": 420000, "Cena (MP+T) - EN": 420000,
     "Počet MJ (MP) - CZ": 25.0, "Počet MJ (MP+T) - CZ": 25.0, "Cena (MP) - CZ": 350000, "Cena (MP+T) - CZ": 350000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 2. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 30.0, "Počet MJ (MP+T) - EN": 30.0, "Cena (MP) - EN": 420000, "Cena (MP+T) - EN": 420000,
     "Počet MJ (MP) - CZ": 25.0, "Počet MJ (MP+T) - CZ": 25.0, "Cena (MP) - CZ": 350000, "Cena (MP+T) - CZ": 350000},
    
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 3. SW", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 30.0, "Počet MJ (MP+T) - EN": 30.0, "Cena (MP) - EN": 420000, "Cena (MP+T) - EN": 420000,
     "Počet MJ (MP) - CZ": 25.0, "Počet MJ (MP+T) - CZ": 25.0, "Cena (MP) - CZ": 350000, "Cena (MP+T) - CZ": 350000},

    # Vyhlášení výsledků SW
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Procesní ukončení soutěže", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 3.0, "Cena (MP) - EN": 42000, "Cena (MP+T) - EN": 42000,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 42000, "Cena (MP+T) - CZ": 42000},
    
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Podpora v navazujících fázích projektu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 5.0, "Počet MJ (MP+T) - EN": 10.0, "Cena (MP) - EN": 70000, "Cena (MP+T) - EN": 140000,
     "Počet MJ (MP) - CZ": 5.0, "Počet MJ (MP+T) - CZ": 10.0, "Cena (MP) - CZ": 70000, "Cena (MP+T) - CZ": 140000},

    # PR podpora v průběhu celé soutěže
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná komunikace projektu (včetně tiskových zpráv)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 17.0, "Počet MJ (MP+T) - EN": 17.0, "Cena (MP) - EN": 238000, "Cena (MP+T) - EN": 238000,
     "Počet MJ (MP) - CZ": 13.0, "Počet MJ (MP+T) - CZ": 13.0, "Cena (MP) - CZ": 182000, "Cena (MP+T) - CZ": 182000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná aktualizace webu", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 3.0, "Cena (MP) - EN": 42000, "Cena (MP+T) - EN": 42000,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 42000, "Cena (MP+T) - CZ": 42000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Soutěžní katalog (struktura, obsah)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 5.0, "Počet MJ (MP+T) - EN": 5.0, "Cena (MP) - EN": 70000, "Cena (MP+T) - EN": 70000,
     "Počet MJ (MP) - CZ": 4.0, "Počet MJ (MP+T) - CZ": 4.0, "Cena (MP) - CZ": 56000, "Cena (MP+T) - CZ": 56000},
    
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Výstava vítězních návrhů (příprava, struktura, obsah, produkční zajištění, instalace)", "Jednotka": "den", "Cena za jednotku": 14000.0,
     "Počet MJ (MP) - EN": 5.0, "Počet MJ (MP+T) - EN": 5.0, "Cena (MP) - EN": 70000, "Cena (MP+T) - EN": 70000,
     "Počet MJ (MP) - CZ": 5.0, "Počet MJ (MP+T) - CZ": 5.0, "Cena (MP) - CZ": 70000, "Cena (MP+T) - CZ": 70000},

    # Další náklady - externí dodavatelé
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Produkcční náklady SW (pronájmy sálů pro SW, tisk, občerstvení, technické zajištění)", "Jednotka": "SW", "Cena za jednotku": 60000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 3.0, "Cena (MP) - EN": 180000, "Cena (MP+T) - EN": 180000,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 180000, "Cena (MP+T) - CZ": 180000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Ubytování zahraničních porotců", "Jednotka": "noc", "Cena za jednotku": 5500.0,
     "Počet MJ (MP) - EN": 9.0, "Počet MJ (MP+T) - EN": 9.0, "Cena (MP) - EN": 49500, "Cena (MP+T) - EN": 49500,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 0.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 0},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Cestovné pro zahraniční porotce", "Jednotka": "cesta", "Cena za jednotku": 7000.0,
     "Počet MJ (MP) - EN": 18.0, "Počet MJ (MP+T) - EN": 18.0, "Cena (MP) - EN": 126000, "Cena (MP+T) - EN": 126000,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 0.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 0},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Překlady čeština/angličtina", "Jednotka": "strana textu", "Cena za jednotku": 500.0,
     "Počet MJ (MP) - EN": 450.0, "Počet MJ (MP+T) - EN": 700.0, "Cena (MP) - EN": 225000, "Cena (MP+T) - EN": 350000,
     "Počet MJ (MP) - CZ": 10.0, "Počet MJ (MP+T) - CZ": 10.0, "Cena (MP) - CZ": 5000, "Cena (MP+T) - CZ": 5000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Fotodokumentace celé soutěže (včetně zákresovách fotografií a dokumentace SW)", "Jednotka": "soubor", "Cena za jednotku": 65000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 65000, "Cena (MP+T) - EN": 65000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 65000, "Cena (MP+T) - CZ": 65000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba vizuálního stylu grafickým studiem", "Jednotka": "soubor", "Cena za jednotku": 55000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 55000, "Cena (MP+T) - EN": 55000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 55000, "Cena (MP+T) - CZ": 55000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba webu soutěže", "Jednotka": "soubor", "Cena za jednotku": 95000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 95000, "Cena (MP+T) - EN": 95000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 95000, "Cena (MP+T) - CZ": 95000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafická úprava a sazba soutěžních podmínek a zadání", "Jednotka": "soubor", "Cena za jednotku": 35000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 35000, "Cena (MP+T) - EN": 35000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 35000, "Cena (MP+T) - CZ": 35000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování katalogu", "Jednotka": "soubor", "Cena za jednotku": 50000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 50000, "Cena (MP+T) - EN": 50000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 50000, "Cena (MP+T) - CZ": 50000},
    
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování výstavy", "Jednotka": "soubor", "Cena za jednotku": 70000.0,
     "Počet MJ (MP) - EN": 1.0, "Počet MJ (MP+T) - EN": 1.0, "Cena (MP) - EN": 70000, "Cena (MP+T) - EN": 70000,
     "Počet MJ (MP) - CZ": 1.0, "Počet MJ (MP+T) - CZ": 1.0, "Cena (MP) - CZ": 70000, "Cena (MP+T) - CZ": 70000},

    # Odměny
    {"Fáze": "Odměny", "Aktivita": "Odměny zahraničních porotců", "Jednotka": "odměna celková", "Cena za jednotku": 255000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 3.0, "Cena (MP) - EN": 765000, "Cena (MP+T) - EN": 765000,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 0.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Odměny českých porotců", "Jednotka": "hod", "Cena za jednotku": 1800.0,
     "Počet MJ (MP) - EN": 192.0, "Počet MJ (MP+T) - EN": 192.0, "Cena (MP) - EN": 345600, "Cena (MP+T) - EN": 345600,
     "Počet MJ (MP) - CZ": 384.0, "Počet MJ (MP+T) - CZ": 384.0, "Cena (MP) - CZ": 691200, "Cena (MP+T) - CZ": 691200},
    
    {"Fáze": "Odměny", "Aktivita": "Odměny odborníků poroty", "Jednotka": "hod", "Cena za jednotku": 1800.0,
     "Počet MJ (MP) - EN": 192.0, "Počet MJ (MP+T) - EN": 256.0, "Cena (MP) - EN": 345600, "Cena (MP+T) - EN": 460800,
     "Počet MJ (MP) - CZ": 192.0, "Počet MJ (MP+T) - CZ": 256.0, "Cena (MP) - CZ": 345600, "Cena (MP+T) - CZ": 460800},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - mezinárodní soutěž", "Jednotka": "odměna pro tým", "Cena za jednotku": 1000000.0,
     "Počet MJ (MP) - EN": 5.0, "Počet MJ (MP+T) - EN": 5.0, "Cena (MP) - EN": 5000000, "Cena (MP+T) - EN": 5000000,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 0.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - mezinárodní soutěž", "Jednotka": "odměna pro tým", "Cena za jednotku": 1000000.0,
     "Počet MJ (MP) - EN": 3.0, "Počet MJ (MP+T) - EN": 3.0, "Cena (MP) - EN": 3000000, "Cena (MP+T) - EN": 3000000,
     "Počet MJ (MP) - CZ": 0.0, "Počet MJ (MP+T) - CZ": 0.0, "Cena (MP) - CZ": 0, "Cena (MP+T) - CZ": 0},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - soutěž v češtině", "Jednotka": "odměna pro tým", "Cena za jednotku": 750000.0,
     "Počet MJ (MP) - EN": 0.0, "Počet MJ (MP+T) - EN": 0.0, "Cena (MP) - EN": 0, "Cena (MP+T) - EN": 0,
     "Počet MJ (MP) - CZ": 5.0, "Počet MJ (MP+T) - CZ": 5.0, "Cena (MP) - CZ": 3750000, "Cena (MP+T) - CZ": 3750000},
    
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - soutěž v češtině", "Jednotka": "odměna pro tým", "Cena za jednotku": 750000.0,
     "Počet MJ (MP) - EN": 0.0, "Počet MJ (MP+T) - EN": 0.0, "Cena (MP) - EN": 0, "Cena (MP+T) - EN": 0,
     "Počet MJ (MP) - CZ": 3.0, "Počet MJ (MP+T) - CZ": 3.0, "Cena (MP) - CZ": 2250000, "Cena (MP+T) - CZ": 2250000}
]

# --- Vytvoření DataFrame ---
df = pd.DataFrame(activities_data)

# --- Výpočet hodnot na základě výběru ---
if variant == "Mezinárodní soutěžní workshop":
    variant_suffix = "EN"
else:
    variant_suffix = "CZ"

if unit_type == "Počet jednotek (změna MP)":
    unit_col = f"Počet MJ (MP) - {variant_suffix}"
    price_col = f"Cena (MP) - {variant_suffix}"
else:
    unit_col = f"Počet MJ (MP+T) - {variant_suffix}"
    price_col = f"Cena (MP+T) - {variant_suffix}"

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
selected_activities = edited_df[edited_df['Vybrané'] == True].copy()
selected_activities['Náklady'] = selected_activities['Upravené množství'] * selected_activities['Upravená cena za jednotku']
total_selected_cost = selected_activities['Náklady'].sum()

# --- Všetky fázy v pôvodnom poradí ---
phase_order = [
    'Analytická fáze',
    'Přípravní fáze',
    'Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW',
    'PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé',
    'Odměny'
]

# --- Pridaj chýbajúce fázy s nulovými hodnotami ---
phase_costs = selected_activities.groupby('Fáze')['Náklady'].sum().reindex(phase_order, fill_value=0)

# --- Optimalizované grafy ---
st.markdown("""
<div class="chart-container">
    <h3 style="text-align: center; color: #059669; margin-bottom: 2rem;">Vizualizace nákladů</h3>
</div>
""", unsafe_allow_html=True)

# Sunburst chart - hierarchie fázy -> aktivity
if len(selected_activities) > 0:
    fig_sunburst = px.sunburst(
        selected_activities,
        path=['Fáze', 'Aktivita'],
        values='Náklady',
        title="Hierarchické rozložení nákladů",
        color='Fáze',
        color_discrete_map={
            'Analytická fáze': '#059669',
            'Přípravní fáze': '#10b981',
            'Průběh soutěžního workshopu (SW)': '#dc2626',
            'Vyhlášení výsledků SW': '#7c3aed',
            'PR podpora v průběhu celé soutěže': '#ea580c',
            'Další náklady - externí dodavatelé': '#0891b2',
            'Odměny': '#be185d'
        }
    )
    fig_sunburst.update_layout(
        title_x=0.5,
        title_font_size=22,
        title_font_color='#059669',
        height=700,
        margin=dict(t=80, l=0, r=0, b=0),
        paper_bgcolor='rgba(255,255,255,0.98)',
        font=dict(family='Inter, sans-serif', size=18, color='#1e2937')
    )
    fig_sunburst.update_traces(
        hovertemplate='<b>%{label}</b><br>Celkové náklady: %{value:,.0f} Kč<extra></extra>',
        marker=dict(line=dict(width=3, color='white')),
        insidetextorientation='radial',
        textfont_size=16,
        textfont_color='white',
        textfont_family='Inter, sans-serif'
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #6b7280; font-size: 1.1rem;">
        <p>Žádné aktivity nejsou vybrány. Vyberte alespoň jednu aktivitu pro zobrazení grafu.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Funkcia na generovanie PDF ---
def generate_pdf_report(selected_activities, total_cost, variant, unit_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=60, leftMargin=60, topMargin=48, bottomMargin=48)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    font_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
    dejavu_path = os.path.join(font_dir, 'DejaVuSans.ttf')
    dejavu_bold_path = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
    if not os.path.exists(dejavu_path) or not os.path.exists(dejavu_bold_path):
        raise FileNotFoundError(
            f"Chýbajúci font! Nahrajte súbory 'DejaVuSans.ttf' a 'DejaVuSans-Bold.ttf' do priečinka 'fonts/' v repozitári. "
            f"Cesty hľadaných súborov: {dejavu_path}, {dejavu_bold_path}"
        )
    pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_path))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_bold_path))
    font_name = 'DejaVuSans'
    font_bold = 'DejaVuSans-Bold'
    styles = getSampleStyleSheet()
    # --- Decentné, vzdušné štýly ---
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=HexColor('#059669'),
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName=font_bold,
        leading=26,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=HexColor('#10b981'),
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName=font_bold,
        leading=16,
    )
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=heading_style,
        fontSize=12,
        textColor=HexColor('#059669'),
        alignment=TA_LEFT,
        spaceAfter=3,
        fontName=font_bold,
        leading=14,
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#1e2937'),
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName=font_name,
    )
    activity_style = ParagraphStyle(
        'ActivitySmall',
        parent=normal_style,
        fontSize=9,
        leading=11,
        spaceAfter=1,
    )
    number_style = ParagraphStyle(
        'NumberRight',
        parent=normal_style,
        fontSize=9,
        leading=11,
        alignment=TA_RIGHT,
    )
    notes_style = ParagraphStyle(
        'Notes',
        parent=normal_style,
        fontSize=8,
        leading=10,
        alignment=TA_LEFT,
        backColor=HexColor('#f3f4f6'),
    )
    sum_style = ParagraphStyle(
        'SumBold',
        parent=normal_style,
        fontSize=10,
        leading=12,
        alignment=TA_RIGHT,
        textColor=HexColor('#059669'),
        fontName=font_bold,
    )
    meta_style = ParagraphStyle(
        'Meta',
        parent=normal_style,
        fontSize=7,
        textColor=HexColor('#6b7280'),
        alignment=TA_RIGHT,
        spaceAfter=1,
    )
    story = []
    # Metaúdaje vpravo hore
    story.append(Paragraph(f"<b>Generované:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}", meta_style))
    story.append(Spacer(1, 1))
    # Logo na stred, menšie
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo web color.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=90, height=28)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 4))
    # Hlavný nadpis
    story.append(Paragraph("Kalkulátor soutěžního workshopu", title_style))
    story.append(Spacer(1, 1))
    # Podnadpisy
    story.append(Paragraph(f"<b>Varianta:</b> {variant}", normal_style))
    story.append(Paragraph(f"<b>Typ jednotek:</b> {unit_type}", normal_style))
    story.append(Spacer(1, 4))
    # Oddelenie sekcie pásikom (jemný)
    story.append(Table(
        [['']],
        colWidths=[5.2*inch],
        style=[('BACKGROUND', (0, 0), (-1, -1), HexColor('#e0f7ef')), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]
    ))
    story.append(Spacer(1, 3))
    # Shrnutí
    story.append(Paragraph("Shrnutí projektu", section_heading_style))
    summary_data = [
        ['Metrika', 'Hodnota'],
        ['Celkové náklady', f"<b><font color='#059669'>{total_cost:,.0f} Kč</font></b>"],
        ['Počet aktivit', f"<b>{len(selected_activities)}</b>"],
        ['Průměrná cena na aktivitu', f"<b>{total_cost / len(selected_activities):,.0f} Kč</b>" if len(selected_activities) > 0 else "0 Kč"]
    ]
    summary_table = Table(summary_data, colWidths=[1.5*inch, 2.2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e0f7ef')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#059669')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
        ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#e5e7eb')),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))
    # Detailné sekcie
    if len(selected_activities) > 0:
        story.append(Paragraph("Detailní rozpis aktivit", section_heading_style))
        phase_groups = selected_activities.groupby('Fáze')
        for phase, phase_activities in phase_groups:
            # Oddelenie sekcie pásikom
            story.append(Spacer(1, 3))
            story.append(Table(
                [['']],
                colWidths=[5.2*inch],
                style=[('BACKGROUND', (0, 0), (-1, -1), HexColor('#f3f4f6')), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]
            ))
            story.append(Spacer(1, 2))
            story.append(Paragraph(f"Fáze: {phase}", heading_style))
            table_data = [
                [
                    Paragraph('Aktivita', heading_style),
                    Paragraph('Množství', heading_style),
                    Paragraph('Cena za jednotku', heading_style),
                    Paragraph('Náklady', heading_style),
                    Paragraph('Poznámky', heading_style)
                ]
            ]
            for _, activity in phase_activities.iterrows():
                table_data.append([
                    Paragraph(str(activity['Aktivita']), activity_style),
                    Paragraph(f"{activity['Upravené množství']:.1f}", number_style),
                    Paragraph(f"{activity['Upravená cena za jednotku']:,.0f} Kč", number_style),
                    Paragraph(f"{activity['Náklady']:,.0f} Kč", number_style),
                    Paragraph(str(activity['Poznámky']) if pd.notna(activity['Poznámky']) else '', notes_style)
                ])
            phase_total = phase_activities['Náklady'].sum()
            table_data.append([
                Paragraph('', normal_style),
                Paragraph('', normal_style),
                Paragraph('SOUČET FÁZE:', sum_style),
                Paragraph(f"{phase_total:,.0f} Kč", sum_style),
                Paragraph('', normal_style)
            ])
            activity_table = Table(table_data, colWidths=[1.7*inch, 0.6*inch, 1.0*inch, 1.0*inch, 1.5*inch])
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e0f7ef')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#059669')),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), font_bold),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('TOPPADDING', (0, 0), (-1, 0), 3),
                ('GRID', (0, 0), (-1, -1), 0.3, HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ]
            # Pruhovať riadky decentne
            for i in range(1, len(table_data)-1):
                if i % 2 == 0:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), HexColor('#f3f4f6')))
                else:
                    table_style.append(('BACKGROUND', (0, i), (-1, i), HexColor('#ffffff')))
            # Súčet
            table_style += [
                ('BACKGROUND', (0, -1), (-1, -1), HexColor('#e0f7ef')),
                ('FONTNAME', (0, -1), (-1, -1), font_bold),
                ('TEXTCOLOR', (0, -1), (-1, -1), HexColor('#059669')),
                ('FONTSIZE', (0, -1), (-1, -1), 9),
                ('ALIGN', (2, -1), (3, -1), 'RIGHT'),
                ('LINEABOVE', (0, -1), (-1, -1), 0.7, HexColor('#059669')),
            ]
            activity_table.setStyle(TableStyle(table_style))
            story.append(activity_table)
            story.append(Spacer(1, 4))
    # Vizualizácia nákladov
    if len(selected_activities) > 0:
        story.append(Paragraph("Vizualizace nákladů", section_heading_style))
        story.append(Paragraph("Graf hierarchického rozložení nákladů je dostupný v interaktivní verzi aplikace.", normal_style))
        story.append(Spacer(1, 4))
    # Záver
    story.append(Table(
        [['']],
        colWidths=[5.2*inch],
        style=[('BACKGROUND', (0, 0), (-1, -1), HexColor('#e0f7ef')), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Závěr", section_heading_style))
    story.append(Paragraph(f"Celkové náklady na soutěžní workshop činí <b><font color='#059669'>{total_cost:,.0f} Kč</font></b>.", normal_style))
    story.append(Paragraph("Tento dokument byl automaticky vygenerován kalkulátorem soutěžního workshopu.", normal_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Export ---
st.markdown("""
<div class="phase-header">
    <h3>Export dat</h3>
</div>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Export do Excel", type="primary"):
        # Vytvorenie Excel súboru
        output = BytesIO()
        
        # Vytvorenie Excel writer
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            selected_activities.to_excel(writer, sheet_name='Vybrané aktivity', index=False)
            if len(selected_activities) > 0:
                avg_cost = total_selected_cost / len(selected_activities)
            else:
                avg_cost = 0
            summary_data = {
                'Metrika': ['Celkové náklady', 'Počet aktivit', 'Průměrná cena na aktivitu'],
                'Hodnota': [
                    f"{total_selected_cost:,.0f} Kč",
                    len(selected_activities),
                    f"{avg_cost:,.0f} Kč"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Shrnutí', index=False)
        
        # Reset pozície v BytesIO
        output.seek(0)
        
        # Stiahnutie súboru
        st.download_button(
            label="Stáhnout Excel soubor",
            data=output.getvalue(),
            file_name=f"kalkulace_soutezniho_workshopu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
with col2:
    if st.button("Export do PDF", type="primary"):
        if len(selected_activities) > 0:
            pdf_buffer = generate_pdf_report(selected_activities, total_selected_cost, variant, unit_type)
            st.download_button(
                label="Stáhnout PDF report",
                data=pdf_buffer.getvalue(),
                file_name=f"kalkulace_soutezniho_workshopu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Pro generování PDF reportu vyberte alespoň jednu aktivitu.")
with col3:
    if st.button("Reset hodnot"):
        st.rerun()

# --- Sticky summary ---
if len(selected_activities) > 0:
    avg_cost = total_selected_cost / len(selected_activities)
    st.markdown(f"""
    <div class="sticky-summary">
        Celkové náklady: {total_selected_cost:,.0f} Kč | Vybrané aktivity: {len(selected_activities)} | Průměrná cena: {avg_cost:,.0f} Kč
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="sticky-summary">
        Celkové náklady: 0 Kč | Vybrané aktivity: 0 | Průměrná cena: 0 Kč
    </div>
    """, unsafe_allow_html=True)
