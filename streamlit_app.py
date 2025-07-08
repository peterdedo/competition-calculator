# ... predchádzajúci kód ostáva ...

# Upravený CSS pre kompaktnejšie fázy a aktivity
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
</style>
""", unsafe_allow_html=True)

# ... hlavný nadpis, varianty, unit_type ...

# Zoskupenie aktivít podľa fáz
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
                st.markdown(f"<div class='activity-details'>Jednotka: {row['Jednotka']}<br>"
                            f"Cena za jednotku: <span class='price-highlight'>{row['Cena za jednotku']:,} Kč</span></div>", unsafe_allow_html=True)
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
        st.markdown(f"<div class='success-card'><strong>💰 Fáze {faze}:</strong> {faze_total:,} Kč</div>", unsafe_allow_html=True)
