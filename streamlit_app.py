# =============================================================================
# KALKULÁTOR SOUTĚŽNÍHO WORKSHOPU - OPTIMALIZOVANÁ VERZIA
# =============================================================================

# --- Importy ---
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import matplotlib.pyplot as plt
import numpy as np

# --- Konštanty ---
PHASES = [
    'Analytická fáze',
    'Přípravní fáze', 
    'Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW',
    'PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé',
    'Odměny'
]

PHASE_COLORS = {
    'Analytická fáze': '#059669',
    'Přípravní fáze': '#10b981',
    'Průběh soutěžního workshopu (SW)': '#dc2626',
    'Vyhlášení výsledků SW': '#7c3aed',
    'PR podpora v průběhu celé soutěže': '#ea580c',
    'Další náklady - externí dodavatelé': '#0891b2',
    'Odměny': '#be185d'
}

# --- Konfigurácia aplikácie ---
PAGE_CONFIG = {
    'page_title': "Kalkulátor soutěžního workshopu",
    'page_icon': "🏗️",
    'layout': "wide"
}

# --- Dáta aktivít ---
ACTIVITIES_DATA = [
    # Analytická fáze
    {"Fáze": "Analytická fáze", "Aktivita": "Sestavení řídící skupiny", "Množství": 1.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Analytická fáze", "Aktivita": "Vymezení řešeného území", "Množství": 1.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Analytická fáze", "Aktivita": "Seznámení se s dostupnými materiály a záměry v území", "Množství": 6.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Analytická fáze", "Aktivita": "Analýza stavu území na základě předem definovaných parametrů a indikátorů", "Množství": 32.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Analytická fáze", "Aktivita": "Kompletace výstupu z analýzy jako podkladu pro zadání soutěže", "Množství": 8.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Analytická fáze", "Aktivita": "Nalezení dohody aktérů (podpis memoranda o shodě na záměru v území)", "Množství": 3.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},

    # Přípravní fáze
    {"Fáze": "Přípravní fáze", "Aktivita": "Návrh procesu soutěže (harmonogram, návrh pracovní a konzultační skupiny)", "Množství": 15.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení podrobného rozpočtu", "Množství": 3.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Identifikace hlavních aktérů a návrh jejich zapojení do procesu (včetně moderace diskuzí)", "Množství": 10.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Komunikace s veřejností (návrh procesu, organizace, zpracování výstupů)", "Množství": 0.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Vytvoření značky soutěže (včetně konzultace se zadavatelem)", "Množství": 4.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "PR strategie projektu", "Množství": 4.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace zadání (parametry využití území, stavební program, průběžná jednání s ŘS a PS)", "Množství": 30.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Formulace soutěžních podmínek", "Množství": 16.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Finalizace a publikace soutěžních podmínek a zadání", "Množství": 4.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Sestavení poroty", "Množství": 6.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Přípravní fáze", "Aktivita": "Kompletace před vyhlášením soutěže a ustavující schůze poroty (včetně regulérnosti ČKA)", "Množství": 23.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},

    # Průběh soutěžního workshopu (SW)
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Vyhlášení soutěže – otevřená výzva a výběr soutěžících", "Množství": 7.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 1. SW", "Množství": 30.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 2. SW", "Množství": 30.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Průběh soutěžního workshopu (SW)", "Aktivita": "Příprava a organizace 3. SW", "Množství": 30.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},

    # Vyhlášení výsledků SW
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Procesní ukončení soutěže", "Množství": 3.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "Vyhlášení výsledků SW", "Aktivita": "Podpora v navazujících fázích projektu", "Množství": 5.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},

    # PR podpora v průběhu celé soutěže
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná komunikace projektu (včetně tiskových zpráv)", "Množství": 17.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Průběžná aktualizace webu", "Množství": 3.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Soutěžní katalog (struktura, obsah)", "Množství": 5.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},
    {"Fáze": "PR podpora v průběhu celé soutěže", "Aktivita": "Výstava vítězních návrhů (příprava, struktura, obsah, produkční zajištění, instalace)", "Množství": 5.0, "Cena za jednotku": 14000.0, "Jednotka": "den"},

    # Další náklady - externí dodavatelé
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Produkcční náklady SW (pronájmy sálů pro SW, tisk, občerstvení, technické zajištění)", "Množství": 3.0, "Cena za jednotku": 60000.0, "Jednotka": "SW"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Ubytování zahraničních porotců", "Množství": 9.0, "Cena za jednotku": 5500.0, "Jednotka": "noc"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Cestovné pro zahraniční porotce", "Množství": 18.0, "Cena za jednotku": 7000.0, "Jednotka": "cesta"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Překlady čeština/angličtina", "Množství": 450.0, "Cena za jednotku": 500.0, "Jednotka": "strana textu"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Fotodokumentace celé soutěže (včetně zákresovách fotografií a dokumentace SW)", "Množství": 1.0, "Cena za jednotku": 65000.0, "Jednotka": "soubor"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba vizuálního stylu grafickým studiem", "Množství": 1.0, "Cena za jednotku": 55000.0, "Jednotka": "soubor"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Tvorba webu soutěže", "Množství": 1.0, "Cena za jednotku": 95000.0, "Jednotka": "soubor"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafická úprava a sazba soutěžních podmínek a zadání", "Množství": 1.0, "Cena za jednotku": 35000.0, "Jednotka": "soubor"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování katalogu", "Množství": 1.0, "Cena za jednotku": 50000.0, "Jednotka": "soubor"},
    {"Fáze": "Další náklady - externí dodavatelé", "Aktivita": "Grafické zpracování výstavy", "Množství": 1.0, "Cena za jednotku": 70000.0, "Jednotka": "soubor"},

    # Odměny
    {"Fáze": "Odměny", "Aktivita": "Odměny zahraničních porotců", "Množství": 3.0, "Cena za jednotku": 255000.0, "Jednotka": "odměna celková"},
    {"Fáze": "Odměny", "Aktivita": "Odměny českých porotců", "Množství": 192.0, "Cena za jednotku": 1800.0, "Jednotka": "hod"},
    {"Fáze": "Odměny", "Aktivita": "Odměny odborníků poroty", "Množství": 192.0, "Cena za jednotku": 1800.0, "Jednotka": "hod"},
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - mezinárodní soutěž", "Množství": 5.0, "Cena za jednotku": 1000000.0, "Jednotka": "odměna pro tým"},
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - mezinárodní soutěž", "Množství": 3.0, "Cena za jednotku": 1000000.0, "Jednotka": "odměna pro tým"},
    {"Fáze": "Odměny", "Aktivita": "Skicovné 1. fáze (1. + 2. SW) - soutěž v češtině", "Množství": 5.0, "Cena za jednotku": 750000.0, "Jednotka": "odměna pro tým"},
    {"Fáze": "Odměny", "Aktivita": "Skicovné 2. fáze (3. SW) - soutěž v češtině", "Množství": 3.0, "Cena za jednotku": 750000.0, "Jednotka": "odměna pro tým"}
]

# --- Pomocné funkcie ---
def create_activities_dataframe():
    """Vytvorí DataFrame s aktivitami z konštánt"""
    return pd.DataFrame(ACTIVITIES_DATA)

def calculate_costs(df, variant_multiplier, unit_type_multiplier):
    """Vypočíta náklady na základe multiplikátorov"""
    df = df.copy()
    df['Upravené množství'] = df['Množství'] * variant_multiplier
    df['Upravená cena za jednotku'] = df['Cena za jednotku'] * unit_type_multiplier
    df['Náklady'] = df['Upravené množství'] * df['Upravená cena za jednotku']
    return df

def get_phase_summary(df):
    """Vráti súhrn nákladov podľa fáz"""
    phase_costs = df.groupby('Fáze')['Náklady'].sum().reindex(PHASES, fill_value=0)
    return phase_costs

def create_sunburst_chart(df):
    """Vytvorí sunburst graf s hierarchiou fázy -> aktivity"""
    if df.empty:
        return go.Figure()
    
    # Vytvoríme hierarchiu fázy -> aktivity
    fig_data = []
    for _, row in df.iterrows():
        fig_data.append({
            'ids': [f"{row['Fáze']}", f"{row['Fáze']}-{row['Aktivita']}"],
            'labels': [row['Fáze'], row['Aktivita']],
            'parents': ['', row['Fáze']],
            'values': [row['Náklady'], row['Náklady']],
            'customdata': [[row['Fáze'], f"{row['Náklady']:,.0f} Kč"], 
                          [row['Aktivita'], f"{row['Náklady']:,.0f} Kč"]]
        })
    
    # Zoskupíme dáta
    all_ids = []
    all_labels = []
    all_parents = []
    all_values = []
    all_customdata = []
    
    for data in fig_data:
        all_ids.extend(data['ids'])
        all_labels.extend(data['labels'])
        all_parents.extend(data['parents'])
        all_values.extend(data['values'])
        all_customdata.extend(data['customdata'])
    
    fig = go.Figure(go.Sunburst(
        ids=all_ids,
        labels=all_labels,
        parents=all_parents,
        values=all_values,
        customdata=all_customdata,
        hovertemplate='<b>%{label}</b><br>Náklady: %{customdata[1]}<extra></extra>',
        branchvalues='total',
        marker=dict(colors=[PHASE_COLORS.get(label, '#6b7280') for label in all_labels]),
        textinfo='label+value'
    ))
    
    fig.update_layout(
        title={
            'text': 'Rozložení nákladů podle fází a aktivit',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#059669'}
        },
        width=800,
        height=600,
        margin=dict(t=80, l=20, r=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# --- Funkcia na generovanie PDF faktúry ---
def generate_invoice_pdf(selected_activities, total_cost, variant, unit_type):
    """Generuje PDF faktúru s detailným rozpisom"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Štýly
    title_style = ParagraphStyle('CustomTitle', 
                                parent=styles['Heading1'], 
                                fontSize=24, 
                                spaceAfter=30, 
                                alignment=TA_CENTER, 
                                textColor=colors.HexColor('#059669'))
    
    heading_style = ParagraphStyle('CustomHeading', 
                                  parent=styles['Heading2'], 
                                  fontSize=16, 
                                  spaceAfter=12, 
                                  textColor=colors.HexColor('#059669'))
    
    # Hlavička
    story.append(Paragraph("KALKULACE SOUTĚŽNÍHO WORKSHOPU", title_style))
    story.append(Spacer(1, 20))
    
    # Informácie o projekte
    project_info = [
        ["Dátum:", datetime.now().strftime("%d.%m.%Y")],
        ["Variant:", variant],
        ["Typ jednotiek:", unit_type],
        ["Celkové náklady:", f"{total_cost:,.0f} Kč"],
        ["Počet aktivit:", str(len(selected_activities))]
    ]
    
    project_table = Table(project_info, colWidths=[2*inch, 4*inch])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#059669')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(project_table)
    story.append(Spacer(1, 30))
    
    # Graf podľa fáz
    if len(selected_activities) > 0:
        story.append(Paragraph("ROZLOŽENÍ NÁKLADŮ PODLE FÁZ", heading_style))
        story.append(Spacer(1, 15))
        
        plt.figure(figsize=(8, 4))
        phase_costs = get_phase_summary(selected_activities)
        plt.pie(phase_costs.values, 
                labels=phase_costs.index, 
                autopct='%1.1f%%', 
                colors=[PHASE_COLORS[p] for p in PHASES], 
                startangle=90)
        plt.title('Rozložení nákladů podle fází', 
                 fontsize=16, 
                 fontweight='bold', 
                 color='#059669')
        plt.axis('equal')
        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        img = Image(img_buffer)
        img.drawHeight = 3*inch
        img.drawWidth = 5*inch
        story.append(img)
        story.append(Spacer(1, 20))
    
    # Detailný rozpis
    story.append(Paragraph("DETAILNÍ ROZPIS AKTIVIT", heading_style))
    story.append(Spacer(1, 15))
    
    table_data = [['Fáze', 'Aktivita', 'Množství', 'Cena za jednotku', 'Celková cena']]
    for _, row in selected_activities.iterrows():
        table_data.append([
            row['Fáze'], 
            row['Aktivita'], 
            f"{row['Upravené množství']:.1f}", 
            f"{row['Upravená cena za jednotku']:,.0f} Kč", 
            f"{row['Náklady']:,.0f} Kč"
        ])
    
    table = Table(table_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (1, -1), 'LEFT'),
    ]))
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Súhrn
    story.append(Paragraph("SOUHRN", heading_style))
    story.append(Spacer(1, 15))
    
    avg_cost = total_cost/len(selected_activities) if len(selected_activities) > 0 else 0
    summary_data = [
        ['Celkové náklady:', f"{total_cost:,.0f} Kč"],
        ['Počet aktivit:', str(len(selected_activities))],
        ['Průměrná cena na aktivitu:', f"{avg_cost:,.0f} Kč"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#059669')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(summary_table)
    
    # Pätička
    story.append(Spacer(1, 40))
    footer_style = ParagraphStyle('Footer', 
                                 parent=styles['Normal'], 
                                 fontSize=10, 
                                 alignment=TA_CENTER, 
                                 textColor=colors.grey)
    story.append(Paragraph("4ct platform", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.set_page_config(**PAGE_CONFIG)

# --- CSS Štýly ---
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
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(5,150,105,0.08);
        border: 1px solid rgba(5,150,105,0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(5,150,105,0.12);
    }
    .metric-card h3 {
        color: #059669;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card h2 {
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    .metric-card p {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
    }
    .phase-header {
        background: linear-gradient(120deg, #059669 0%, #10b981 100%);
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        color: white;
        margin: 2rem 0 1rem 0;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 8px 32px rgba(5,150,105,0.15);
    }
    .progress-bar {
        height: 4px;
        background: linear-gradient(90deg, #059669 0%, #10b981 50%, #34d399 100%);
        border-radius: 2px;
        margin: 2rem 0;
        animation: shimmer 2s ease-in-out infinite;
    }
    @keyframes shimmer {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    .chart-container {
        background: rgba(255,255,255,0.95);
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(5,150,105,0.08);
        border: 1px solid rgba(5,150,105,0.1);
    }
    .sticky-summary {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        box-shadow: 0 12px 48px rgba(5,150,105,0.25);
        z-index: 1000;
        min-width: 300px;
        backdrop-filter: blur(10px);
    }
    .sticky-summary h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
        font-weight: 700;
    }
    .sticky-summary .total-cost {
        font-size: 2rem;
        font-weight: 900;
        margin: 0.5rem 0;
    }
    .sticky-summary .activity-count {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --- Hlavička aplikácie ---
st.markdown("""
<div class="main-header">
    <div class="hero-bg"></div>
    <h1>Kalkulátor soutěžního workshopu</h1>
    <p>Profesionální nástroj pro kalkulaci nákladů architektonických soutěží</p>
    <div class="brand-logo">4ct platform</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Nastavení</div>', unsafe_allow_html=True)
    
    # Variant
    variant = st.radio(
        "Vyberte variant:",
        ["CZ", "SK"],
        help="Vyberte variant pro kalkulaci."
    )
    
    # Typ jednotiek
    unit_type = st.radio(
        "Typ jednotek:",
        ["Počet jednotek (změna MP)", "Počet jednotek (MP+T)"],
        help="Vyberte typ jednotek pro kalkulaci."
    )

# --- Inicializace dat ---
df = create_activities_dataframe()

# --- Přidání sloupců pro editaci ---
df['Vybrané'] = True
df['Upravené množství'] = df['Množství']  # Použijeme základní množství
df['Upravená cena za jednotku'] = df['Cena za jednotku']  # Použijeme základní cenu
df['Poznámky'] = ''

# --- Nastavení multiplikátorů podle variantu ---
if variant == "SK":
    variant_multiplier = 1.2  # 20% navýšení pro SK
else:
    variant_multiplier = 1.0  # Základní cena pro CZ
    
if unit_type == "Počet jednotek (změna MP)":
    unit_multiplier = 1.0  # Základní množství
else:
    unit_multiplier = 1.1  # 10% navýšení pro MP+T

# --- Aplikování multiplikátorů ---
df['Upravené množství'] = df['Množství'] * unit_multiplier
df['Upravená cena za jednotku'] = df['Cena za jednotku'] * variant_multiplier

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

# --- KPI karty ---
col1, col2, col3 = st.columns(3)
with col1:
    total_cost = (filtered_df['Upravené množství'] * filtered_df['Upravená cena za jednotku']).sum()
    st.markdown(f"""
    <div class="metric-card">
        <h3>Celkové náklady</h3>
        <h2>{total_cost:,.0f} Kč</h2>
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
    avg_cost = (filtered_df['Upravené množství'] * filtered_df['Upravená cena za jednotku']).mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>Průměrná cena</h3>
        <h2>{avg_cost:,.0f} Kč</h2>
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

# --- Všechny fáze v původním pořadí ---
phase_order = [
    'Analytická fáze',
    'Přípravní fáze',
    'Průběh soutěžního workshopu (SW)',
    'Vyhlášení výsledků SW',
    'PR podpora v průběhu celé soutěže',
    'Další náklady - externí dodavatelé',
    'Odměny'
]

# --- Přidej chybějící fáze s nulovými hodnotami ---
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
        font=dict(family='Inter, sans-serif', size=18, color='#1e293b')
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

# --- Export ---
st.markdown("""
<div class="phase-header">
    <h3>Export dat</h3>
</div>
""", unsafe_allow_html=True)

# Excel Export
if st.button("📊 Export do Excel", type="primary", use_container_width=True):
    output = BytesIO()
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
    output.seek(0)
    st.download_button(
        label="📥 Stáhnout Excel soubor",
        data=output.getvalue(),
        file_name=f"kalkulace_soutezniho_workshopu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# PDF Export
if len(selected_activities) > 0:
    try:
        pdf_buffer = generate_invoice_pdf(selected_activities, total_selected_cost, variant, unit_type)
        st.download_button(
            label="📄 Stáhnout PDF faktúru",
            data=pdf_buffer.getvalue(),
            file_name=f"faktura_soutezniho_workshopu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.success("✅ PDF faktúra je připravena ke stažení!")
    except Exception as e:
        st.error(f"❌ Chyba při generování PDF: {str(e)}")
else:
    st.error("❌ Pro export do PDF je potřeba vybrat alespoň jednu aktivitu.")

# Reset
if st.button("🔄 Reset hodnot", use_container_width=True):
    st.rerun()

# --- Sticky summary ---
if len(selected_activities) > 0:
    st.markdown(f"""
    <div class="sticky-summary">
        <h4>📊 Aktuální souhrn</h4>
        <div class="total-cost">{total_selected_cost:,.0f} Kč</div>
        <div class="activity-count">{len(selected_activities)} aktivit vybráno</div>
    </div>
    """, unsafe_allow_html=True)

