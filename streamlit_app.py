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
        # Analytická fáze
        {"Fáze":"Analytická fáze","Aktivita":"Sestavení řídící skupiny","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":1,"MP jednotky - CZ":1,"MP+TP jednotky - MEZ":2,"MP+TP jednotky - CZ":2},
        {"Fáze":"Analytická fáze","Aktivita":"Vymezení řešeného území","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":1,"MP jednotky - CZ":1,"MP+TP jednotky - MEZ":2,"MP+TP jednotky - CZ":2},
        {"Fáze":"Analytická fáze","Aktivita":"Seznámení se s dostupnými materiály a záměry v území","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":6,"MP jednotky - CZ":6,"MP+TP jednotky - MEZ":8,"MP+TP jednotky - CZ":8},
        {"Fáze":"Analytická fáze","Aktivita":"Analýza stavu území na základě předem definovaných parametrů a indikátorů","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":32,"MP jednotky - CZ":32,"MP+TP jednotky - MEZ":42,"MP+TP jednotky - CZ":42},
        {"Fáze":"Analytická fáze","Aktivita":"Kompletace výstupu z analýzy jako podkladu pro zadání soutěže","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":8,"MP jednotky - CZ":8,"MP+TP jednotky - MEZ":11,"MP+TP jednotky - CZ":11},
        {"Fáze":"Analytická fáze","Aktivita":"Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":3,"MP jednotky - CZ":3,"MP+TP jednotky - MEZ":6,"MP+TP jednotky - CZ":6},
        # Přípravní fáze
        {"Fáze":"Přípravní fáze","Aktivita":"Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":15,"MP jednotky - CZ":15,"MP+TP jednotky - MEZ":20,"MP+TP jednotky - CZ":20},
        {"Fáze":"Přípravní fáze","Aktivita":"Sestavení podrobného rozpočtu","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":3,"MP jednotky - CZ":2,"MP+TP jednotky - MEZ":4,"MP+TP jednotky - CZ":3},
        {"Fáze":"Přípravní fáze","Aktivita":"Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":10,"MP jednotky - CZ":10,"MP+TP jednotky - MEZ":15,"MP+TP jednotky - CZ":15},
        {"Fáze":"Přípravní fáze","Aktivita":"Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":0,"MP jednotky - CZ":0,"MP+TP jednotky - MEZ":15,"MP+TP jednotky - CZ":15},
        {"Fáze":"Přípravní fáze","Aktivita":"Vytvoření značky soutěže (včetně konzultace se zadavatelem)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":4,"MP jednotky - CZ":4,"MP+TP jednotky - MEZ":4,"MP+TP jednotky - CZ":4},
        {"Fáze":"Přípravní fáze","Aktivita":"PR strategie projektu","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":4,"MP jednotky - CZ":3,"MP+TP jednotky - MEZ":4,"MP+TP jednotky - CZ":3},
        {"Fáze":"Přípravní fáze","Aktivita":"Kompletace zadání (parametry využití území, stavební program, průběžná jednávání s ŘS a PS)","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":30,"MP jednotky - CZ":25,"MP+TP jednotky - MEZ":50,"MP+TP jednotky - CZ":40},
        {"Fáze":"Přípravní fáze","Aktivita":"Formulace soutěžních podmínek","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":16,"MP jednotky - CZ":16,"MP+TP jednotky - MEZ":20,"MP+TP jednotky - CZ":20},
        {"Fáze":"Přípravní fáze","Aktivita":"Finalizace a publikace soutěžních podmínek a zadání","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":4,"MP jednotky - CZ":4,"MP+TP jednotky - MEZ":5,"MP+TP jednotky - CZ":5},
        {"Fáze":"Přípravní fáze","Aktivita":"Sestavení poroty","Jednotka":"den","Cena za jednotku":14000,"MP jednotky - MEZ":6,"MP jednotky - CZ":5,"MP+TP jednotky - MEZ":9,"
