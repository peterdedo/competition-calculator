import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Kalkulátor soutěžního workshopu", layout="wide")

st.title("Kalkulátor soutěžního workshopu")
st.markdown("Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže")

variant = st.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    horizontal=True
)

activities_data = [
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
        "Fáze": "Přípravní fáze",
        "Aktivita": "Návrh procesu soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5,
        "MP jednotky - CZ": 5
    }
]

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
    if st.button("Export do Excel"):
        df = pd.DataFrame(selected_activities)
        df.to_excel("rozpocet.xlsx", index=False)
        st.success("Rozpočet byl exportován do 'rozpocet.xlsx'")
else:
    st.info("Vyberte alespoň jednu aktivitu pro zobrazení celkových nákladů")

st.markdown("---")
st.markdown(f"*Vytvořeno pomocí Streamlit | {datetime.now().strftime('%d.%m.%Y %H:%M')}*")
