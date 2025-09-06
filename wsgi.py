import sys
import os

# Add your project directory to the sys.path
project_home = '/home/aniket34742/Voice-Translator'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = '/home/aniket34742/voice-translator-env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Flask app
from app import app as application
