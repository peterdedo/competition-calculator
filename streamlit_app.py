# V priečinku projektu
cd /Users/administrator/Documents/Cursor/4ct_project

# Inicializujte Git (ak ešte nie je)
git init

# Pridajte súbory
git add app.py requirements.txt

# Commit
git commit -m "Initial commit"

# Pridajte remote
git remote add origin https://github.com/peterdedo/competition-calculator.git

# Push
git branch -M main
git push -u origin main
