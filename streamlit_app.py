import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Moderný a kompaktný dizajn
st.set_page_config(
    page_title="🏆 Kalkulátor soutěžního workshopu",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kompaktnejší CSS
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
</style>
""", unsafe_allow_html=True)

# Hlavný nadpis
st.markdown("""
<div class="main-header">
    <h1>🏆 Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů na architektonické soutěže</p>
    <p style="font-size: 0.9rem; opacity: 0.9;">Vyberte aktivity a nastavte množství pro každou fázi projektu</p>
</div>
""", unsafe_allow_html=True)

# Výber varianty
st.markdown("""
<div class="variant-selector">
    <h3>🎯 Výběr varianty soutěže</h3>
    <p style="margin: 0; opacity: 0.9;">Mezinárodní variant zahrnuje zahraniční porotce a anglické materiály</p>
</div>
""", unsafe_allow_html=True)

variant = st.radio(
    "Vyberte variantu:",
    ["🇪🇺 Mezinárodní soutěžní workshop", "🇨🇿 Soutěžní workshop v češtině"],
    horizontal=True,
    help="Mezinárodní variant zahrnuje zahraniční porotce a anglické materiály"
)

# Globálny výber typu jednotiek
unit_type = st.radio(
    "Vyberte typ jednotek pro rozpočet:",
    ["Počet jednotek (změna MP)", "Počet jednotek (změna MP + transformační plochy)"],
    horizontal=True,
    help="Vyberte, zda chcete počítat pouze změnu MP, nebo i transformační plochy."
)

# Príklad dát (pridajte ďalšie stĺpce podľa potreby)
activities_data = [
    # Príklad: doplňte podľa vašich potrieb a Excelu
    {
        "Fáze": "Analytická fáze",
        "Aktivita": "Sestavení řídící skupiny",
        "Jednotka": "den",
        "Cena za jednotku": 14000,
        "MP jednotky - MEZ": 1, "MP+TP jednotky - MEZ": 2,
        "Cena MP - MEZ": 14000, "Cena MP+TP - MEZ": 28000,
        "MP jednotky - CZ": 1, "MP+TP jednotky - CZ": 2,
        "Cena MP - CZ": 14000, "Cena MP+TP - CZ": 28000
    },
    # ... ďalšie aktivity podľa vašich potrieb ...
]

selected_activities = []
total = 0
selected_count = 0
total_activities = len(activities_data)
faze_totals = {}

df = pd.DataFrame(activities_data)
fazes = df["Fáze"].unique()

for faze in fazes:
    st.markdown(f"<div class='phase-header'>{faze}</div>", unsafe_allow_html=True)
    faze_df = df[df["Fáze"] == faze]
    faze_total = 0

    for i, row in faze_df.iterrows():
        with st.expander(f"{row['Aktivita']}", expanded=False):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
            with col1:
                st.markdown(
                    f"<div class='activity-details'>Jednotka: {row['Jednotka']}<br>"
                    f"Cena za jednotku: <span class='price-highlight'>{row['Cena za jednotku']:,} Kč</span></div>",
                    unsafe_allow_html=True
                )
            # Dynamicky podľa varianty a unit_type
            if variant == "🇪🇺 Mezinárodní soutěžní workshop":
                if unit_type == "Počet jednotek (změna MP)":
                    jednotky_default = int(row.get("MP jednotky - MEZ", 0))
                    cena_za_aktivitu = row.get("Cena MP - MEZ", jednotky_default * row["Cena za jednotku"])
                else:
                    jednotky_default = int(row.get("MP+TP jednotky - MEZ", 0))
                    cena_za_aktivitu = row.get("Cena MP+TP - MEZ", jednotky_default * row["Cena za jednotku"])
            else:
                if unit_type == "Počet jednotek (změna MP)":
                    jednotky_default = int(row.get("MP jednotky - CZ", 0))
                    cena_za_aktivitu = row.get("Cena MP - CZ", jednotky_default * row["Cena za jednotku"])
                else:
                    jednotky_default = int(row.get("MP+TP jednotky - CZ", 0))
                    cena_za_aktivitu = row.get("Cena MP+TP - CZ", jednotky_default * row["Cena za jednotku"])
            cena_za_jednotku = row["Cena za jednotku"]
            if jednotky_default > 0:
                cena_za_jednotku = int(cena_za_aktivitu / jednotky_default)
            with col2:
                jednotky = st.number_input(
                    "Jednotek",
                    min_value=0,
                    value=jednotky_default,
                    key=f"units_{faze}_{i}_{unit_type}_{variant}"
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
                    "Jednotka": row['Jednotka'],
                    "Množství": jednotky,
                    "Cena za jednotku": cena_za_jednotku,
                    "Subtotal": subtotal
                })
                faze_total += subtotal
                total += subtotal
    if faze_total > 0:
        st.markdown(f"<div class='status-indicator status-selected'><strong>💰 Fáze {faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)

# Progress bar
progress = selected_count / total_activities if total_activities else 0
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
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        fig_pie = px.pie(
            df_selected.groupby('Fáze')['Subtotal'].sum().reset_index(),
            values='Subtotal',
            names='Fáze',
            title='Rozložení nákladů podle fází',
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
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        fig_bar = px.bar(
            df_selected,
            x='Aktivita',
            y='Subtotal',
            color='Fáze',
            title='Náklady podle aktivit',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_bar.update_xaxes(tickangle=45)
        fig_bar.update_layout(
            title_font_size=16,
            title_font_color="#2c3e50",
            xaxis_title="Aktivita",
            yaxis_title="Náklady (Kč)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Celkové výsledky
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
    # Export
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
        st.info("📄 PDF export bude implementován v další verzi")
else:
    st.markdown("""
    <div class="warning-card">
        <h3>⚠️ Vyberte alespoň jednu aktivitu pro zobrazení celkových nákladů</h3>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏆 Kalkulátor soutěžního workshopu | Vytvořeno s pomocí Streamlit</p>
    <p>{datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
</div>
""", unsafe_allow_html=True)
