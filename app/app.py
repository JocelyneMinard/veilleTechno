import sys
import os
from flask import Flask, flash, redirect, render_template, url_for
import pandas


path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if path_projet not in sys.path:
    sys.path.insert(0, path_projet)

from services import take_mister_auto_data, take_oscaro_data

app = Flask(__name__)

app.config["SECRET_KEY"] = "une_cle_secrete_tres_securisee"

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/", methods=['POST'])
def index_post():
    try:
        take_mister_auto_data()
        take_oscaro_data()
        flash(
            "Recuperation réussie ! ",
            "success",
        )
        # 3. On redirige sur la page du formulaire au lieu d'une autre page
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Erreur lors de l'excecution : {str(e)}", "danger")
        return redirect(url_for("index"))

@app.route('/view', methods=['GET'])
def view_excel():
    file = os.path.join(path_projet, "Book.xlsx")
    try:
        # Lire le fichier Excel directement depuis la mémoire avec Pandas
        content_file = pandas.read_excel(file, sheet_name="Veille concurrentielle")
        # Convertir le DataFrame en tableau HTML
        data = content_file.to_html(classes ='table', border ="0", index=False)
        print(data)
        
        return render_template("data.html", data = data)
    except FileNotFoundError:
            return f"Le fichier 'Book.xlsx' est introuvable dans le dossier {path_projet}", 404

if __name__ == "__main__":
    app.run(debug=True)
    