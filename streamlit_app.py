import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurácia stránky
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    layout="wide"
)

# Hlavný nadpis
st.title("Kalkulátor soutěžního workshopu")
st.markdown("Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže")

# Výběr varianty
variant = st.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    horizontal=True
)

# Kompletné dáta so všetkými fázami
activities_data = [
    # Analytická fáze
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Sestavení řídící skupiny",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1,
        "MP jednotky - CZ": 1
    },
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Vymezení řešeného území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1,
        "MP jednotky - CZ": 1
    },
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Seznámení se s dostupnými materiály a záměry v území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6,
        "MP jednotky - CZ": 6
    },
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Analýza stavu území na základě předem definovaných parametrů",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8,
        "MP jednotky - CZ": 8
    },
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3,
        "MP jednotky - CZ": 3
    },
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Nalezení dohody aktérů (memorandum o shodě)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4,
        "MP jednotky - CZ": 4
    },
    
    # Přípravní fáze
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Návrh procesu soutěže (harmonogram, pracovní skupiny)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Sestavení podrobného rozpočtu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3,
        "MP jednotky - CZ": 3
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Identifikace aktérů a návrh jejich zapojení",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4,
        "MP jednotky - CZ": 4
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Komunikace s veřejností",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6,
        "MP jednotky - CZ": 6
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Vytvoření značky soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3,
        "MP jednotky - CZ": 3
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "PR strategie projektu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4,
        "MP jednotky - CZ": 4
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Kompletace zadání (včetně stavebního programu)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 7,
        "MP jednotky - CZ": 7
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Formulace soutěžních podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Finalizace a publikace podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2,
        "MP jednotky - CZ": 2
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Sestavení poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3,
        "MP jednotky - CZ": 3
    },
    {
        "Fáze": "Přípravní fáze",
        "Aktivita": "Ustavující schůze poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1,
        "MP jednotky - CZ": 1
    },
    
    # Průběh SW
    {
        "Fáze": "Průběh SW",
        "Aktivita": "Vyhlášení soutěže a výběr účastníků",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2,
        "MP jednotky - CZ": 2
    },
    {
        "Fáze": "Průběh SW",
        "Aktivita": "Příprava a organizace 1. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    },
    {
        "Fáze": "Průběh SW",
        "Aktivita": "Příprava a organizace 2. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    },
    {
        "Fáze": "Průběh SW",
        "Aktivita": "Příprava a organizace 3. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    },
    
    # Vyhlášení výsledků
    {
        "Fáze": "Vyhlášení výsledků",
        "Aktivita": "Ukončení soutěže a podpora další fáze",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3,
        "MP jednotky - CZ": 3
    },
    
    # PR podpora
    {
        "Fáze": "PR podpora",
        "Aktivita": "Tiskové zprávy, web, katalog, výstava",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8,
        "MP jednotky - CZ": 8
    },
    
    # Externí náklady
    {
        "Fáze": "Externí náklady",
        "Aktivita": "Ubytování, překlady, grafika, web",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 10,
        "MP jednotky - CZ": 10
    },
    
    # Odměny
    {
        "Fáze": "Odměny",
        "Aktivita": "Odměny porotcům a účastníkům",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 15,
        "MP jednotky - CZ": 15
    }
]

# Zobrazení aktivit
selected_activities = []
total = 0

for i, activity in enumerate(activities_data):
    with st.expander(f"{activity['Aktivita']}", expanded=False):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**Fáze:** {activity['Fáze']}")
            st.write(f"**Jednotka:** {activity['Jednotka']}")
            st.write(f"**Cena za jednotku:** {activity['Cena za jednotku']:,} Kč")
        
        with col2:
            if variant == "Mezinárodní soutěžní workshop":
                jednotky = st.number_input("Množství", min_value=0, value=activity["MP jednotky - MEZ"], key=f"units_{i}")
            else:
                jednotky = st.number_input("Množství", min_value=0, value=activity["MP jednotky - CZ"], key=f"units_{i}")
        
        with col3:
            subtotal = jednotky * activity['Cena za jednotku']
            st.write(f"**Subtotal:** {subtotal:,} Kč")
            
            if jednotky > 0:
                selected_activities.append({
                    "Fáze": activity["Fáze"],
                    "Aktivita": activity["Aktivita"],
                    "Množství": jednotky,
                    "Cena za jednotku": activity["Cena za jednotku"],
                    "Subtotal": subtotal
                })
                total += subtotal

# Celkové výsledky
if selected_activities:
    st.markdown("---")
    st.header("Celkové náklady")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Celková suma bez DPH", f"{total:,} Kč")
    
    with col2:
        vat_amount = total * 0.21
        st.metric("DPH (21%)", f"{vat_amount:,} Kč")
    
    with col3:
        total_with_vat = total * 1.21
        st.metric("Celková suma s DPH", f"{total_with_vat:,} Kč")
    
    # Export
    if st.button("Export do Excel"):
        df = pd.DataFrame(selected_activities)
        df.to_excel("rozpocet.xlsx", index=False)
        st.success("Rozpočet byl exportován do 'rozpocet.xlsx'")

else:
    st.info("Vyberte alespoň jednu aktivitu pro zobrazení celkových nákladů")

# Footer
st.markdown("---")
st.markdown(f"*Vytvořeno pomocí Streamlit | {datetime.now().strftime('%d.%m.%Y %H:%M')}*")
