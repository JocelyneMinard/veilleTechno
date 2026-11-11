import sys
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas


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

@app.route('/view', methods=['GET'])
def view_excel():
    file = os.path.join(path_projet, "Book.xlsx")
    try:
        # Lire le fichier Excel directement depuis la mémoire avec Pandas
        content_file = pandas.read_excel(file)
        # Convertir le DataFrame en tableau HTML
        data = content_file.to_html(classes ='table', border ="0", index=False)
        print(data)
        
        return render_template("data.html", data = data)
    except FileNotFoundError:
            return f"Le fichier 'Book.xlsx' est introuvable dans le dossier {path_projet}", 404

if __name__ == "__main__":
    app.run(debug=True)
    