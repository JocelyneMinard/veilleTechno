import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import load_workbook
import sys
import os

def take_auto_doc_data():

    path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    if path_projet not in sys.path:
        sys.path.insert(0, path_projet)


    produits = [
        ("Filtre a huile Purflux","https://www.auto-doc.fr/purflux/7852205?search=PURFLUX+Filtre+%C3%A0+huile+%28LS280A%29", 2),
        ("Amortisseur TRW", "https://www.auto-doc.fr/trw/2199141?search=TRW+Amortisseur+%28JHT264T%29 ", 3),
        ("Plaquettes Valeo", "https://www.auto-doc.fr/valeo/7949921?search=VALEO+Plaquettes+de+frein+%28301007%29", 4)
    ]

    classeur = load_workbook(os.path.join(path_projet, "Book.xlsx"))
    feuille = classeur["Veille concurrentielle"]

    driver = webdriver.Chrome()

    try:
        for nom, url, ligne in produits:
            try:
                driver.get(url)

                element = driver.find_element(By.CSS_SELECTOR, ".large-price--std")

                prix = element.get_attribute("textContent")
                prix = float(prix.replace("€", "").replace("\xa0", "").replace(",", ".").strip())

                feuille.cell(row=ligne, column=4).value = prix

                print(nom, ":", prix, "€")

            except Exception:
                print(nom, ": prix introuvable, ancien prix conservé")

    finally:
        driver.quit()

    classeur.save(os.path.join(path_projet, "Book.xlsx"))
    print("Fichier Excel mis à jour !")
