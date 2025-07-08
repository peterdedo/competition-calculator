# Prejdite do priečinka projektu
cd /Users/administrator/Documents/Cursor/4ct_project

# Inicializujte Git (ak ešte nie je)
git init

# Pridajte len potrebné súbory
git add app.py requirements.txt

# Vytvorte .gitignore pre nepotrebné súbory
echo "venv/
.venv/
__pycache__/
*.pyc
*.xlsx
.DS_Store" > .gitignore

# Pridajte .gitignore
git add .gitignore

# Vytvorte prvý commit
git commit -m "Initial commit - Competition calculator app"

# Pridajte remote repozitár
git remote add origin https://github.com/peterdedo/competition-calculator.git

# Nahrajte na GitHub
git branch -M main
git push -u origin main

# Pridajte nový súbor
git add streamlit_app.py

# Commit zmeny
git commit -m "Create new clean streamlit_app.py"

# Push na GitHub
git push
