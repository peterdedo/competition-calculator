# Prejdite do priečinka s vašou aplikáciou
cd /Users/administrator/Documents/Cursor/4ct_project

# Inicializujte Git repozitár
git init

# Pridajte súbory
git add competition_calculator_clean.py

# Vytvorte requirements.txt pre Streamlit
echo "streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
openpyxl>=3.0.0" > requirements.txt

# Pridajte requirements.txt
git add requirements.txt

# Vytvorte prvý commit
git commit -m "Initial commit - Competition calculator app"

# Pridajte remote repozitár (nahraďte YOUR_USERNAME a REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Nahrajte kód na GitHub
git branch -M main
git push -u origin main
