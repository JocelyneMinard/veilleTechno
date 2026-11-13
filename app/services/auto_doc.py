from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver
from openpyxl import load_workbook
import os
import random
import re
import sys
import time

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
    driver = Driver(uc=True)

    try:
        for nom, url, ligne in produits:
            try:
                # Ouvre l'URL en déconnectant brièvement le pilote pour passer Cloudflare
                driver.uc_open_with_reconnect(url.strip(), reconnect_time=5)

                WebDriverWait(driver, 30).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".product-card__price-wrap"), "€")
                )
                element = driver.find_element(By.CSS_SELECTOR, ".product-card__price-wrap")

                texte_prix = element.get_attribute("textContent")
                match = re.search(r"(\d+\s*[.,]\s*\d+)", texte_prix)
              
                if match:
                    prix_propre = re.sub(r"\s+", "", match.group(1)).replace(",", ".")
                    prix = float(prix_propre)
                    feuille.cell(row=ligne, column=4).value = prix
                    print(f"{nom} : {prix} €")

                # Pause naturelle entre deux fiches produits
                time.sleep(random.uniform(3, 6))

            except Exception:
                print(nom, ": prix introuvable, ancien prix conservé")

    finally:
        driver.quit()

    classeur.save(os.path.join(path_projet, "Book.xlsx"))
    print("Fichier Excel mis à jour !")



if __name__ == "__main__":
    take_auto_doc_data()