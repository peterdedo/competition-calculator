# Vytvorte nový priečinok
mkdir competition-calculator-clean
cd competition-calculator-clean

# Skopírujte len správne súbory
cp ../4ct_project/app.py .
cp ../4ct_project/requirements.txt .

# Vytvorte nový Git repozitár
git init
git add .
git commit -m "Initial commit - clean version"

# Vytvorte nový repozitár na GitHub
# Choďte na GitHub a vytvorte repozitár: peterdedo/competition-calculator-clean

# Nahrajte kód
git remote add origin https://github.com/peterdedo/competition-calculator-clean.git
git push -u origin main
