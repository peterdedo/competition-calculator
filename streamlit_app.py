import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

# Konfigurácia stránky s moderným dizajnom
st.set_page_config(
    page_title="🏆 Kalkulátor soutěžního workshopu",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pre moderný vzhled
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
    .expander-header {
        font-weight: 600;
        font-size: 1.05rem;
        color: #2c3e50;
    }
    .activity-details {
        color: #7f8c8d;
        font-size: 0.92rem;
        margin-bottom: 0.3rem;
    }
    .price-highlight {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e74c3c;
    }
    .status-indicator {
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-selected {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .status-unselected {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
    }
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 10px;
        border-radius: 5px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .variant-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        display: inline-block;
    }
    .variant-mez {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
    }
    .variant-cz {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
    }
    .type-badge {
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 0.1rem;
        display: inline-block;
    }
    .type-mp {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .type-mp-tp {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Hlavný nadpis s moderným dizajnom
st.markdown("""
<div class="main-header">
    <h1>🏆 Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">Kompletní přehled všech variant a typů aktivit</p>
</div>
""", unsafe_allow_html=True)

# Výber varianty a typu jednotiek
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

# Kompletné dáta so všetkými fázami a variantmi
activities_data = [
    # Analytická fáze
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "👥 Sestavení řídící skupiny",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🗺️ Vymezení řešeného území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "📋 Seznámení se s dostupnými materiály a záměry v území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6,
        "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
        "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000,
        "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🔍 Analýza stavu území na základě předem definovaných parametrů",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8,
        "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
        "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000,
        "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "📝 Kompletace výstupu z analýzy jako podkladu pro zadání soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🤝 Nalezení dohody aktérů (memorandum o shodě)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    
    # Přípravní fáze
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📅 Návrh procesu soutěže (harmonogram, pracovní skupiny)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "💰 Sestavení podrobného rozpočtu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "👤 Identifikace aktérů a návrh jejich zapojení",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📢 Komunikace s veřejností",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6,
        "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
        "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000,
        "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "🎨 Vytvoření značky soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📈 PR strategie projektu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📋 Kompletace zadání (včetně stavebního programu)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 7, "MP jednotky - CZ": 7,
        "MP+TP jednotky - MEZ": 10.5, "MP+TP jednotky - CZ": 10.5,
        "Cena MP - MEZ": 98000, "Cena MP - CZ": 98000,
        "Cena MP+TP - MEZ": 147000, "Cena MP+TP - CZ": 147000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📜 Formulace soutěžních podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "✅ Finalizace a publikace podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2,
        "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
        "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000,
        "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "👨‍⚖️ Sestavení poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "🏛️ Ustavující schůze poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    
    # Průběh SW
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "📢 Vyhlášení soutěže a výběr účastníků",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2,
        "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
        "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000,
        "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 1. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 2. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 3. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    
    # Vyhlášení výsledků
    {
        "Fáze": "🏆 Vyhlášení výsledků",
        "Aktivita": "🎉 Ukončení soutěže a podpora další fáze",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    
    # PR podpora
    {
        "Fáze": "📰 PR podpora",
        "Aktivita": "📺 Tiskové zprávy, web, katalog, výstava",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8,
        "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
        "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000,
        "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000
    },
    
    # Externí náklady
    {
        "Fáze": "💼 Externí náklady",
        "Aktivita": "🏨 Ubytování, překlady, grafika, web",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 10, "MP jednotky - CZ": 10,
        "MP+TP jednotky - MEZ": 15, "MP+TP jednotky - CZ": 15,
        "Cena MP - MEZ": 140000, "Cena MP - CZ": 140000,
        "Cena MP+TP - MEZ": 210000, "Cena MP+TP - CZ": 210000
    },
    
    # Odměny
    {
        "Fáze": "💰 Odměny",
        "Aktivita": "🏆 Odměny porotcům a účastníkům",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 15, "MP jednotky - CZ": 15,
        "MP+TP jednotky - MEZ": 22.5, "MP+TP jednotky - CZ": 22.5,
        "Cena MP - MEZ": 210000, "Cena MP - CZ": 210000,
        "Cena MP+TP - MEZ": 315000, "Cena MP+TP - CZ": 315000
    }
]

# Zobrazení aktivit s moderným dizajnom - všetky varianty a typy naraz
selected_activities = []
total = 0
selected_count = 0
total_activities = len(activities_data) * 4  # 4 kombinácie pre každú aktivitu
faze_totals = {}

# Zoskupenie aktivít podľa fáz
df = pd.DataFrame(activities_data)
fazes = df["Fáze"].unique()

# Kľúče podľa výberu
if variant == "Mezinárodní soutěžní workshop":
    vkey = "MEZ"
else:
    vkey = "CZ"
if unit_type == "Počet jednotek (změna MP)":
    ukey = "MP"
else:
    ukey = "MP+TP"

for faze in fazes:
    st.markdown(f"<div class='phase-header'>{faze}</div>", unsafe_allow_html=True)
    faze_df = df[df["Fáze"] == faze]
    faze_total = 0

    for i, row in faze_df.iterrows():
        with st.expander(f"{row['Aktivita']}", expanded=False):
            st.markdown(f"<div class='activity-details'>Jednotka: {row['Jednotka']}<br>"
                        f"Cena za jednotku: <span class='price-highlight'>{row['Cena za jednotku']:,} Kč</span></div>", unsafe_allow_html=True)
            
            # Všetky 4 kombinácie variantov a typov
            variants_data = [
                {"name": "🇪🇺 Mezinárodní - MP", "variant": "MEZ", "type": "MP", "units_key": f"{ukey} jednotky - MEZ", "price_key": f"Cena {ukey} - MEZ"},
                {"name": "🇪🇺 Mezinárodní - MP+TP", "variant": "MEZ", "type": "MP+TP", "units_key": f"{ukey} jednotky - MEZ", "price_key": f"Cena {ukey}+TP - MEZ"},
                {"name": "🇨🇿 Český - MP", "variant": "CZ", "type": "MP", "units_key": f"{ukey} jednotky - CZ", "price_key": f"Cena {ukey} - CZ"},
                {"name": "🇨🇿 Český - MP+TP", "variant": "CZ", "type": "MP+TP", "units_key": f"{ukey} jednotky - CZ", "price_key": f"Cena {ukey}+TP - CZ"}
            ]
            
            for variant_data in variants_data:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    variant_class = "variant-mez" if variant_data["variant"] == "MEZ" else "variant-cz"
                    type_class = "type-mp" if variant_data["type"] == "MP" else "type-mp-tp"
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <span class="variant-badge {variant_class}">{variant_data['name']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Získanie hodnôt pre danú kombináciu
                jednotky_default = int(row.get(variant_data["units_key"], 0))
                cena_za_aktivitu = row.get(variant_data["price_key"], jednotky_default * row["Cena za jednotku"])
                cena_za_jednotku = row["Cena za jednotku"]
                if jednotky_default > 0:
                    cena_za_jednotku = int(cena_za_aktivitu / jednotky_default)
                
                with col2:
                    jednotky = st.number_input(
                        "Jednotek",
                        min_value=0,
                        value=jednotky_default,
                        key=f"units_{faze}_{i}_{variant_data['variant']}_{variant_data['type']}"
                    )
                
                with col3:
                    st.markdown(f"**{jednotky}** {row['Jednotka']}")
                
                with col4:
                    subtotal = jednotky * cena_za_jednotku
                    st.markdown(f"**{subtotal:,} Kč**")
                
                if jednotky > 0:
                    st.markdown(f"<div class='status-indicator status-selected'>✅ Aktivita vybrána</div>", unsafe_allow_html=True)
                    selected_count += 1
                else:
                    st.markdown(f"<div class='status-indicator status-unselected'>⏳ Aktivita nevybrána</div>", unsafe_allow_html=True)
                
                if jednotky > 0:
                    selected_activities.append({
                        "Fáze": faze,
                        "Aktivita": row['Aktivita'],
                        "Variant": variant_data["name"],
                        "Jednotka": row['Jednotka'],
                        "Množství": jednotky,
                        "Cena za jednotku": cena_za_jednotku,
                        "Subtotal": subtotal
                    })
                    faze_total += subtotal
                    total += subtotal
            
            st.markdown("---")
    
    if faze_total > 0:
        faze_totals[faze] = faze_total
        st.markdown(f"<div class='success-card'><strong>💰 Fáze {faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)

# Progress bar
progress = selected_count / total_activities
st.markdown(f"""
<div class="progress-bar" style="width: {progress * 100}%;"></div>
<p style="text-align: center; color: #666; margin: 1rem 0;">
📊 Pokrok: {selected_count}/{total_activities} aktivit vybráno ({progress:.1%})
</p>
""", unsafe_allow_html=True)

# Grafy
if selected_activities:
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>📊 Vizualizace nákladů</h2>
    </div>
    """, unsafe_allow_html=True)
    
    df_selected = pd.DataFrame(selected_activities)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

# Konfigurácia stránky s moderným dizajnom
st.set_page_config(
    page_title="🏆 Kalkulátor soutěžního workshopu",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pre moderný vzhled
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
    .expander-header {
        font-weight: 600;
        font-size: 1.05rem;
        color: #2c3e50;
    }
    .activity-details {
        color: #7f8c8d;
        font-size: 0.92rem;
        margin-bottom: 0.3rem;
    }
    .price-highlight {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e74c3c;
    }
    .status-indicator {
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-selected {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .status-unselected {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
    }
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 10px;
        border-radius: 5px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .variant-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        display: inline-block;
    }
    .variant-mez {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
    }
    .variant-cz {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
    }
    .type-badge {
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: 600;
        margin: 0.1rem;
        display: inline-block;
    }
    .type-mp {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        color: white;
    }
    .type-mp-tp {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Hlavný nadpis s moderným dizajnom
st.markdown("""
<div class="main-header">
    <h1>🏆 Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">Kompletní přehled všech variant a typů aktivit</p>
</div>
""", unsafe_allow_html=True)

# Kompletné dáta so všetkými fázami a variantmi
activities_data = [
    # Analytická fáze
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "👥 Sestavení řídící skupiny",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🗺️ Vymezení řešeného území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "📋 Seznámení se s dostupnými materiály a záměry v území",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6,
        "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
        "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000,
        "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🔍 Analýza stavu území na základě předem definovaných parametrů",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8,
        "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
        "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000,
        "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "📝 Kompletace výstupu z analýzy jako podkladu pro zadání soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📊 Analytická fáze",
        "Aktivita": "🤝 Nalezení dohody aktérů (memorandum o shodě)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    
    # Přípravní fáze
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📅 Návrh procesu soutěže (harmonogram, pracovní skupiny)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "💰 Sestavení podrobného rozpočtu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "👤 Identifikace aktérů a návrh jejich zapojení",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📢 Komunikace s veřejností",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 6, "MP jednotky - CZ": 6,
        "MP+TP jednotky - MEZ": 9, "MP+TP jednotky - CZ": 9,
        "Cena MP - MEZ": 84000, "Cena MP - CZ": 84000,
        "Cena MP+TP - MEZ": 126000, "Cena MP+TP - CZ": 126000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "🎨 Vytvoření značky soutěže",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📈 PR strategie projektu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 4, "MP jednotky - CZ": 4,
        "MP+TP jednotky - MEZ": 6, "MP+TP jednotky - CZ": 6,
        "Cena MP - MEZ": 56000, "Cena MP - CZ": 56000,
        "Cena MP+TP - MEZ": 84000, "Cena MP+TP - CZ": 84000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📋 Kompletace zadání (včetně stavebního programu)",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 7, "MP jednotky - CZ": 7,
        "MP+TP jednotky - MEZ": 10.5, "MP+TP jednotky - CZ": 10.5,
        "Cena MP - MEZ": 98000, "Cena MP - CZ": 98000,
        "Cena MP+TP - MEZ": 147000, "Cena MP+TP - CZ": 147000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "📜 Formulace soutěžních podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "✅ Finalizace a publikace podmínek",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2,
        "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
        "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000,
        "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "👨‍⚖️ Sestavení poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    {
        "Fáze": "📋 Přípravní fáze",
        "Aktivita": "🏛️ Ustavující schůze poroty",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP jednotky - CZ": 1,
        "MP+TP jednotky - MEZ": 1.5, "MP+TP jednotky - CZ": 1.5,
        "Cena MP - MEZ": 14000, "Cena MP - CZ": 14000,
        "Cena MP+TP - MEZ": 21000, "Cena MP+TP - CZ": 21000
    },
    
    # Průběh SW
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "📢 Vyhlášení soutěže a výběr účastníků",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 2, "MP jednotky - CZ": 2,
        "MP+TP jednotky - MEZ": 3, "MP+TP jednotky - CZ": 3,
        "Cena MP - MEZ": 28000, "Cena MP - CZ": 28000,
        "Cena MP+TP - MEZ": 42000, "Cena MP+TP - CZ": 42000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 1. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 2. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    {
        "Fáze": "🎯 Průběh SW",
        "Aktivita": "🏢 Příprava a organizace 3. workshopu",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 5, "MP jednotky - CZ": 5,
        "MP+TP jednotky - MEZ": 7.5, "MP+TP jednotky - CZ": 7.5,
        "Cena MP - MEZ": 70000, "Cena MP - CZ": 70000,
        "Cena MP+TP - MEZ": 105000, "Cena MP+TP - CZ": 105000
    },
    
    # Vyhlášení výsledků
    {
        "Fáze": "🏆 Vyhlášení výsledků",
        "Aktivita": "🎉 Ukončení soutěže a podpora další fáze",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 3, "MP jednotky - CZ": 3,
        "MP+TP jednotky - MEZ": 4.5, "MP+TP jednotky - CZ": 4.5,
        "Cena MP - MEZ": 42000, "Cena MP - CZ": 42000,
        "Cena MP+TP - MEZ": 63000, "Cena MP+TP - CZ": 63000
    },
    
    # PR podpora
    {
        "Fáze": "📰 PR podpora",
        "Aktivita": "📺 Tiskové zprávy, web, katalog, výstava",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 8, "MP jednotky - CZ": 8,
        "MP+TP jednotky - MEZ": 12, "MP+TP jednotky - CZ": 12,
        "Cena MP - MEZ": 112000, "Cena MP - CZ": 112000,
        "Cena MP+TP - MEZ": 168000, "Cena MP+TP - CZ": 168000
    },
    
    # Externí náklady
    {
        "Fáze": "💼 Externí náklady",
        "Aktivita": "🏨 Ubytování, překlady, grafika, web",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 10, "MP jednotky - CZ": 10,
        "MP+TP jednotky - MEZ": 15, "MP+TP jednotky - CZ": 15,
        "Cena MP - MEZ": 140000, "Cena MP - CZ": 140000,
        "Cena MP+TP - MEZ": 210000, "Cena MP+TP - CZ": 210000
    },
    
    # Odměny
    {
        "Fáze": "💰 Odměny",
        "Aktivita": "🏆 Odměny porotcům a účastníkům",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 15, "MP jednotky - CZ": 15,
        "MP+TP jednotky - MEZ": 22.5, "MP+TP jednotky - CZ": 22.5,
        "Cena MP - MEZ": 210000, "Cena MP - CZ": 210000,
        "Cena MP+TP - MEZ": 315000, "Cena MP+TP - CZ": 315000
    }
]

# Zobrazení aktivit s moderným dizajnom - všetky varianty a typy naraz
selected_activities = []
total = 0
selected_count = 0
total_activities = len(activities_data) * 4  # 4 kombinácie pre každú aktivitu
faze_totals = {}

# Zoskupenie aktivít podľa fáz
df = pd.DataFrame(activities_data)
fazes = df["Fáze"].unique()

for faze in fazes:
    st.markdown(f"<div class='phase-header'>{faze}</div>", unsafe_allow_html=True)
    faze_df = df[df["Fáze"] == faze]
    faze_total = 0

    for i, row in faze_df.iterrows():
        with st.expander(f"{row['Aktivita']}", expanded=False):
            st.markdown(f"<div class='activity-details'>Jednotka: {row['Jednotka']}<br>"
                        f"Cena za jednotku: <span class='price-highlight'>{row['Cena za jednotku']:,} Kč</span></div>", unsafe_allow_html=True)
            
            # Všetky 4 kombinácie variantov a typov
            variants_data = [
                {"name": "🇪🇺 Mezinárodní - MP", "variant": "MEZ", "type": "MP", "units_key": "MP jednotky - MEZ", "price_key": "Cena MP - MEZ"},
                {"name": "🇪🇺 Mezinárodní - MP+TP", "variant": "MEZ", "type": "MP+TP", "units_key": "MP+TP jednotky - MEZ", "price_key": "Cena MP+TP - MEZ"},
                {"name": "🇨🇿 Český - MP", "variant": "CZ", "type": "MP", "units_key": "MP jednotky - CZ", "price_key": "Cena MP - CZ"},
                {"name": "🇨🇿 Český - MP+TP", "variant": "CZ", "type": "MP+TP", "units_key": "MP+TP jednotky - CZ", "price_key": "Cena MP+TP - CZ"}
            ]
            
            for variant_data in variants_data:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    variant_class = "variant-mez" if variant_data["variant"] == "MEZ" else "variant-cz"
                    type_class = "type-mp" if variant_data["type"] == "MP" else "type-mp-tp"
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 0.5rem;">
                        <span class="variant-badge {variant_class}">{variant_data['name']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Získanie hodnôt pre danú kombináciu
                jednotky_default = int(row.get(variant_data["units_key"], 0))
                cena_za_aktivitu = row.get(variant_data["price_key"], jednotky_default * row["Cena za jednotku"])
                cena_za_jednotku = row["Cena za jednotku"]
                if jednotky_default > 0:
                    cena_za_jednotku = int(cena_za_aktivitu / jednotky_default)
                
                with col2:
                    jednotky = st.number_input(
                        "Jednotek",
                        min_value=0,
                        value=jednotky_default,
                        key=f"units_{faze}_{i}_{variant_data['variant']}_{variant_data['type']}"
                    )
                
                with col3:
                    st.markdown(f"**{jednotky}** {row['Jednotka']}")
                
                with col4:
                    subtotal = jednotky * cena_za_jednotku
                    st.markdown(f"**{subtotal:,} Kč**")
                
                if jednotky > 0:
                    st.markdown(f"<div class='status-indicator status-selected'>✅ Aktivita vybrána</div>", unsafe_allow_html=True)
                    selected_count += 1
                else:
                    st.markdown(f"<div class='status-indicator status-unselected'>⏳ Aktivita nevybrána</div>", unsafe_allow_html=True)
                
                if jednotky > 0:
                    selected_activities.append({
                        "Fáze": faze,
                        "Aktivita": row['Aktivita'],
                        "Variant": variant_data["name"],
                        "Jednotka": row['Jednotka'],
                        "Množství": jednotky,
                        "Cena za jednotku": cena_za_jednotku,
                        "Subtotal": subtotal
                    })
                    faze_total += subtotal
                    total += subtotal
            
            st.markdown("---")
    
    if faze_total > 0:
        faze_totals[faze] = faze_total
        st.markdown(f"<div class='success-card'><strong>💰 Fáze {faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)

# Progress bar
progress = selected_count / total_activities
st.markdown(f"""
<div class="progress-bar" style="width: {progress * 100}%;"></div>
<p style="text-align: center; color: #666; margin: 1rem 0;">
📊 Pokrok: {selected_count}/{total_activities} aktivit vybráno ({progress:.1%})
</p>
""", unsafe_allow_html=True)

# Grafy
if selected_activities:
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>📊 Vizualizace nákladů</h2>
    </div>
    """, unsafe_allow_html=True)
    
    df_selected = pd.DataFrame(selected_activities)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        # Pie chart pre varianty
        variant_totals = df_selected.groupby('Variant')['Subtotal'].sum().reset_index()
        fig_pie = px.pie(
            variant_totals,
            values='Subtotal',
            names='Variant',
            title='Rozložení nákladů podle variant',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            title_font_size=16,
            title_font_color="#2c3e50",
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        # Bar chart pre fáze
        faze_totals_df = df_selected.groupby('Fáze')['Subtotal'].sum().reset_index()
        fig_bar = px.bar(
            faze_totals_df,
            x='Fáze',
            y='Subtotal',
            title='Náklady podle fází',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_xaxes(tickangle=45)
        fig_bar.update_layout(
            title_font_size=16,
            title_font_color="#2c3e50",
            xaxis_title="Fáze",
            yaxis_title="Náklady (Kč)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Celkové výsledky s moderným dizajnom
st.markdown("---")
st.markdown("""
<div class="main-header">
    <h2>💰 Celkové náklady</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💵 Celková suma bez DPH</h3>
        <h2>{total:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    vat_amount = total * 0.21
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 DPH (21%)</h3>
        <h2>{vat_amount:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_with_vat = total * 1.21
    st.markdown(f"""
    <div class="metric-card">
        <h3>💳 Celková suma s DPH</h3>
        <h2>{total_with_vat:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📋 Počet aktivit</h3>
        <h2>{len(selected_activities)}</h2>
    </div>
    """, unsafe_allow_html=True)

# Detailní přehled
if selected_activities:
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>📋 Detailní přehled aktivit</h2>
    </div>
    """, unsafe_allow_html=True)
    
    df_selected = pd.DataFrame(selected_activities)
    st.dataframe(df_selected, use_container_width=True)
    
    # Export s moderným dizajnem
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>📤 Export výsledků</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export do Excel", key="export_excel"):
            try:
                df_selected.to_excel("soutezni_workshop_rozpocet.xlsx", index=False)
                st.success("✅ Rozpočet byl exportován do 'soutezni_workshop_rozpocet.xlsx'")
            except Exception as e:
                st.error(f"❌ Chyba při exportu: {e}")
    
    with col2:
        if st.button("📄 Export do PDF", key="export_pdf"):
            try:
                # Funkcia pre generovanie PDF
                def generate_pdf_report(df_data, total_data):
                    buffer = BytesIO()
                    doc = SimpleDocTemplate(buffer, pagesize=A4)
                    elements = []
                    
                    # Štýly
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle(
                        'CustomTitle',
                        parent=styles['Heading1'],
                        fontSize=16,
                        spaceAfter=30,
                        alignment=1
                    )
                    
                    # Nadpis
                    elements.append(Paragraph("🏆 Kalkulátor soutěžního workshopu", title_style))
                    elements.append(Spacer(1, 20))
                    
                    # Celkové súčty
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
                    
                    # Detailná tabuľka
                    elements.append(Paragraph("Detailní přehled aktivit:", styles['Heading2']))
                    elements.append(Spacer(1, 10))
                    
                    # Príprava dát pre tabuľku
                    table_data = [['Fáze', 'Aktivita', 'Variant', 'Jednotky', 'Cena (Kč)']]
                    
                    for _, row in df_data.iterrows():
                        table_data.append([
                            row['Fáze'],
                            row['Aktivita'][:30] + '...' if len(row['Aktivita']) > 30 else row['Aktivita'],
                            row['Variant'],
                            str(row['Množství']),
                            f"{row['Subtotal']:,}"
                        ])
                    
                    # Vytvorenie tabuľky s limitom riadkov
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
                    
                    # Zostavenie dokumentu
                    doc.build(elements)
                    buffer.seek(0)
                    return buffer
                
                total_data = {
                    'total': total,
                    'vat': vat_amount,
                    'total_with_vat': total_with_vat
                }
                
                pdf_buffer = generate_pdf_report(df_selected, total_data)
                
                # Vytvorenie download linku
                b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="soutezni_workshop_rozpocet.pdf">📄 Stáhnout PDF report</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("✅ PDF report byl úspěšně vygenerován!")
                
            except Exception as e:
                st.error(f"❌ Chyba při generování PDF: {e}")

else:
    st.markdown("""
    <div class="warning-card">
        <h3>⚠️ Vyberte alespoň jednu aktivitu pro zobrazení celkových nákladů</h3>
    </div>
    """, unsafe_allow_html=True)

# Footer s moderným dizajnom
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏆 Kalkulátor soutěžního workshopu | Vytvořeno pomocí Streamlit</p>
    <p>{}</p>
</div>
""".format(datetime.now().strftime("%d.%m.%Y %H:%M")), unsafe_allow_html=True) 
