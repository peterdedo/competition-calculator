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

# Vytvorenie kompletnej tabuľky so všetkými variantmi a typmi
def create_complete_dataframe():
    complete_data = []
    
    for activity in activities_data:
        # MEZ - MP
        complete_data.append({
            "Fáze": activity["Fáze"],
            "Aktivita": activity["Aktivita"],
            "Jednotka": activity["Jednotka"],
            "Cena za jednotku": activity["Cena za jednotku"],
            "Variant": "🇪🇺 Mezinárodní",
            "Typ jednotek": "MP",
            "Jednotky": activity["MP jednotky - MEZ"],
            "Cena za aktivitu": activity["Cena MP - MEZ"],
            "Subtotal": activity["Cena MP - MEZ"]
        })
        
        # MEZ - MP+TP
        complete_data.append({
            "Fáze": activity["Fáze"],
            "Aktivita": activity["Aktivita"],
            "Jednotka": activity["Jednotka"],
            "Cena za jednotku": activity["Cena za jednotku"],
            "Variant": "🇪🇺 Mezinárodní",
            "Typ jednotek": "MP+TP",
            "Jednotky": activity["MP+TP jednotky - MEZ"],
            "Cena za aktivitu": activity["Cena MP+TP - MEZ"],
            "Subtotal": activity["Cena MP+TP - MEZ"]
        })
        
        # CZ - MP
        complete_data.append({
            "Fáze": activity["Fáze"],
            "Aktivita": activity["Aktivita"],
            "Jednotka": activity["Jednotka"],
            "Cena za jednotku": activity["Cena za jednotku"],
            "Variant": "🇨🇿 Český",
            "Typ jednotek": "MP",
            "Jednotky": activity["MP jednotky - CZ"],
            "Cena za aktivitu": activity["Cena MP - CZ"],
            "Subtotal": activity["Cena MP - CZ"]
        })
        
        # CZ - MP+TP
        complete_data.append({
            "Fáze": activity["Fáze"],
            "Aktivita": activity["Aktivita"],
            "Jednotka": activity["Jednotka"],
            "Cena za jednotku": activity["Cena za jednotku"],
            "Variant": "🇨🇿 Český",
            "Typ jednotek": "MP+TP",
            "Jednotky": activity["MP+TP jednotky - CZ"],
            "Cena za aktivitu": activity["Cena MP+TP - CZ"],
            "Subtotal": activity["Cena MP+TP - CZ"]
        })
    
    return pd.DataFrame(complete_data)

# Vytvorenie kompletnej tabuľky
df_complete = create_complete_dataframe()

# Zobrazenie kompletnej tabuľky
st.markdown("""
<div class="main-header">
    <h2>📊 Kompletní přehled všech variant a typů aktivit</h2>
</div>
""", unsafe_allow_html=True)

# Filtrovanie a zobrazenie
st.markdown("### 🔍 Filtrování a úprava")
col1, col2 = st.columns(2)

with col1:
    selected_fazes = st.multiselect(
        "Vyberte fáze:",
        options=df_complete["Fáze"].unique(),
        default=df_complete["Fáze"].unique()
    )

with col2:
    selected_variants = st.multiselect(
        "Vyberte varianty:",
        options=df_complete["Variant"].unique(),
        default=df_complete["Variant"].unique()
    )

# Filtrovanie dát
df_filtered = df_complete[
    (df_complete["Fáze"].isin(selected_fazes)) &
    (df_complete["Variant"].isin(selected_variants))
]

# Zobrazenie filtrovanej tabuľky s možnosťou editácie
st.markdown("### 📋 Detailní tabulka aktivit")

# Vytvorenie editovateľnej tabuľky
edited_df = st.data_editor(
    df_filtered,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Fáze": st.column_config.TextColumn("Fáze", width="medium"),
        "Aktivita": st.column_config.TextColumn("Aktivita", width="large"),
        "Jednotka": st.column_config.TextColumn("Jednotka", width="small"),
        "Cena za jednotku": st.column_config.NumberColumn("Cena za jednotku (Kč)", format="%d"),
        "Variant": st.column_config.SelectboxColumn("Variant", options=df_complete["Variant"].unique()),
        "Typ jednotek": st.column_config.SelectboxColumn("Typ jednotek", options=df_complete["Typ jednotek"].unique()),
        "Jednotky": st.column_config.NumberColumn("Jednotky", format="%.1f"),
        "Cena za aktivitu": st.column_config.NumberColumn("Cena za aktivitu (Kč)", format="%d"),
        "Subtotal": st.column_config.NumberColumn("Subtotal (Kč)", format="%d")
    }
)

# Výpočet celkových súm
total_by_variant_type = edited_df.groupby(["Variant", "Typ jednotek"])["Subtotal"].sum().reset_index()

st.markdown("### 💰 Celkové náklady podle variant a typů")

# Zobrazenie súm v kartách
for _, row in total_by_variant_type.iterrows():
    variant_class = "variant-mez" if "Mezinárodní" in row["Variant"] else "variant-cz"
    type_class = "type-mp" if row["Typ jednotek"] == "MP" else "type-mp-tp"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{row['Variant']} - {row['Typ jednotek']}</h3>
        <h2>{row['Subtotal']:,} Kč</h2>
        <div style="margin-top: 0.5rem;">
            <span class="variant-badge {variant_class}">{row['Variant']}</span>
            <span class="type-badge {type_class}">{row['Typ jednotek']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Celkové súčty
total_all = edited_df["Subtotal"].sum()
vat_amount = total_all * 0.21
total_with_vat = total_all * 1.21

st.markdown("### 📊 Celkové součty")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💵 Celková suma bez DPH</h3>
        <h2>{total_all:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 DPH (21%)</h3>
        <h2>{vat_amount:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💳 Celková suma s DPH</h3>
        <h2>{total_with_vat:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

# Grafy
if not edited_df.empty:
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>📊 Vizualizace nákladů</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        """, unsafe_allow_html=True)
        # Pie chart pre varianty a typy
        fig_pie = px.pie(
            total_by_variant_type,
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
        fig_bar = px.bar(
            edited_df.groupby('Fáze')['Subtotal'].sum().reset_index(),
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
    table_data = [['Fáze', 'Aktivita', 'Variant', 'Typ', 'Jednotky', 'Cena (Kč)']]
    
    for _, row in df_data.iterrows():
        table_data.append([
            row['Fáze'],
            row['Aktivita'][:30] + '...' if len(row['Aktivita']) > 30 else row['Aktivita'],
            row['Variant'],
            row['Typ jednotek'],
            str(row['Jednotky']),
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

# Export do PDF
st.markdown("---")
st.markdown("""
<div class="main-header">
    <h2>📤 Export výsledků</h2>
</div>
""", unsafe_allow_html=True)

if st.button("📄 Export do PDF", key="export_pdf"):
    try:
        total_data = {
            'total': total_all,
            'vat': vat_amount,
            'total_with_vat': total_with_vat
        }
        
        pdf_buffer = generate_pdf_report(edited_df, total_data)
        
        # Vytvorenie download linku
        b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="soutezni_workshop_rozpocet.pdf">📄 Stáhnout PDF report</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ PDF report byl úspěšně vygenerován!")
        
    except Exception as e:
        st.error(f"❌ Chyba při generování PDF: {e}")

# Footer s moderným dizajnom
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏆 Kalkulátor soutěžního workshopu | Vytvořeno pomocí Streamlit</p>
    <p>{}</p>
</div>
""".format(datetime.now().strftime("%d.%m.%Y %H:%M")), unsafe_allow_html=True) 
