import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Konfigurácia stránky s moderným dizajnom
st.set_page_config(
    page_title="Kalkulátor soutěžního workshopu",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pre moderný vzhled
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .phase-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .activity-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .variant-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 8px;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Hlavný nadpis s moderným dizajnom
st.markdown("""
<div class="main-header">
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
</div>
""", unsafe_allow_html=True)

# Výběr varianty s moderným dizajnem
st.markdown("""
<div class="variant-selector">
    <h3>Výběr varianty soutěže</h3>
</div>
""", unsafe_allow_html=True)

variant = st.radio(
    "Vyberte variantu:",
    ["Mezinárodní soutěžní workshop", "Soutěžní workshop v češtině"],
    horizontal=True,
    help="Mezinárodní variant zahrnuje zahraniční porotce a anglické materiály"
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

# Zobrazení aktivit s moderným dizajnom
selected_activities = []
total = 0
selected_count = 0
total_activities = len(activities_data)
faze_totals = {}

# Zoskupenie aktivít podľa fáz
df = pd.DataFrame(activities_data)
fazes = df["Fáze"].unique()

for faze in fazes:
    st.markdown(f"""
    <div class="phase-header">
        <h3>{faze}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    faze_df = df[df["Fáze"] == faze]
    faze_total = 0

    for i, row in faze_df.iterrows():
        st.markdown(f"""
        <div class="activity-card">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        
        with col1:
            st.markdown(f"**{row['Aktivita']}**")
            st.markdown(f"Jednotka: {row['Jednotka']}")
            st.markdown(f"Cena za jednotku: {row['Cena za jednotku']:,} Kč")
        
        with col2:
            if variant == "Mezinárodní soutěžní workshop":
                jednotky = st.number_input("Jednotek (MP)", min_value=0, value=int(row["MP jednotky - MEZ"]), key=f"mez_mp_{i}")
            else:
                jednotky = st.number_input("Jednotek (MP)", min_value=0, value=int(row["MP jednotky - CZ"]), key=f"cz_mp_{i}")
        
        with col3:
            st.markdown(f"**{jednotky}** {row['Jednotka']}")
        
        with col4:
            subtotal = jednotky * row['Cena za jednotku']
            st.markdown(f"**{subtotal:,} Kč**")
        
        with col5:
            if jednotky > 0:
                st.success("Aktivita vybrána")
                selected_count += 1
            else:
                st.info("Aktivita nevybrána")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if jednotky > 0:
            selected_activities.append({
                "Fáze": faze,
                "Aktivita": row['Aktivita'],
                "Jednotka": row['Jednotka'],
                "Množství": jednotky,
                "Cena za jednotku": row['Cena za jednotku'],
                "Subtotal": subtotal
            })
            faze_total += subtotal
            total += subtotal
    
    if faze_total > 0:
        faze_totals[faze] = faze_total
        st.markdown(f"""
        <div class="success-card">
            <strong>Fáze {faze}:</strong> {faze_total:,} Kč
        </div>
        """, unsafe_allow_html=True)

# Progress bar
progress = selected_count / total_activities
st.markdown(f"""
<div class="progress-bar" style="width: {progress * 100}%;"></div>
<p>Pokrok: {selected_count}/{total_activities} aktivit vybráno ({progress:.1%})</p>
""", unsafe_allow_html=True)

# Grafy
if selected_activities:
    st.markdown("---")
    st.header("Vizualizace nákladů")
    
    df_selected = pd.DataFrame(selected_activities)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart pro fáze
        fig_pie = px.pie(
            df_selected.groupby('Fáze')['Subtotal'].sum().reset_index(),
            values='Subtotal',
            names='Fáze',
            title='Rozložení nákladů podle fází',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart pro aktivity
        fig_bar = px.bar(
            df_selected,
            x='Aktivita',
            y='Subtotal',
            color='Fáze',
            title='Náklady podle aktivit',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)

# Celkové výsledky s moderným dizajnom
st.markdown("---")
st.markdown("""
<div class="main-header">
    <h2>Celkové náklady</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Celková suma bez DPH</h3>
        <h2>{total:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    vat_amount = total * 0.21
    st.markdown(f"""
    <div class="metric-card">
        <h3>DPH (21%)</h3>
        <h2>{vat_amount:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_with_vat = total * 1.21
    st.markdown(f"""
    <div class="metric-card">
        <h3>Celková suma s DPH</h3>
        <h2>{total_with_vat:,} Kč</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Počet aktivit</h3>
        <h2>{len(selected_activities)}</h2>
    </div>
    """, unsafe_allow_html=True)

# Detailní přehled
if selected_activities:
    st.markdown("---")
    st.header("Detailní přehled aktivit")
    
    df_selected = pd.DataFrame(selected_activities)
    st.dataframe(df_selected, use_container_width=True)
    
    # Export s moderným dizajnem
    st.markdown("---")
    st.markdown("""
    <div class="main-header">
        <h2>Export výsledků</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export do Excel", key="export_excel"):
            try:
                df_selected.to_excel("soutezni_workshop_rozpocet.xlsx", index=False)
                st.success("Rozpočet byl exportován do 'soutezni_workshop_rozpocet.xlsx'")
            except Exception as e:
                st.error(f"Chyba při exportu: {e}")
    
    with col2:
        st.info("PDF export bude implementován v další verzi")

else:
    st.markdown("""
    <div class="warning-card">
        <h3>Vyberte alespoň jednu aktivitu pro zobrazení celkových nákladů</h3>
    </div>
    """, unsafe_allow_html=True)

# Footer s moderným dizajnem
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Kalkulátor soutěžního workshopu | Vytvořeno pomocí Streamlit</p>
    <p>{}</p>
</div>
""".format(datetime.now().strftime("%d.%m.%Y %H:%M")), unsafe_allow_html=True)
