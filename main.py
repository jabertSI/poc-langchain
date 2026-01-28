import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

# Chemin vers app.py dans le module
current_dir = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_dir, "my_assistant", "app.py")

if not os.path.isfile(app_path):
    raise FileNotFoundError(f"Le fichier app.py est introuvable : {app_path}")

# Lancer Streamlit
subprocess.run(["streamlit", "run", app_path])
