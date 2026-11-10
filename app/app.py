import sys
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_projet not in sys.path:
    sys.path.insert(0, path_projet)


load_dotenv()
app = Flask(__name__)

# --- Connexion base de données ---
#app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
# Ajoutez une clé secrète (obligatoire pour utiliser flash)
#app.config["SECRET_KEY"] = "une_cle_secrete_tres_securisee"

# Initialisation de l'extension
#db = SQLAlchemy(app)


@app.route("/")
def index():
   return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    