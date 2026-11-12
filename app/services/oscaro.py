import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from openpyxl import load_workbook
import sys
import os


def take_oscaro_data():

    path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    if path_projet not in sys.path:
        sys.path.insert(0, path_projet)

    produits = [
        ("Filtre à huile Purflux", "https://www.oscaro.com/filtre-a-huile-purflux-ls280a-1213708-7-p#/?vid=11408", 2),
        ("Amortisseur TRW", "https://www.oscaro.com/jeu-de-2-amortisseurs-trw-jht264t-1857387-3539-p#/?vid=11408", 3),
        ("Plaquettes Valeo", "https://www.oscaro.com/jeu-de-4-plaquettes-de-frein-valeo-301007-6042068-402-p#/?vid=11408 ", 4)
    ]

    classeur = load_workbook(os.path.join(path_projet, "Book.xlsx"))
    feuille = classeur["Veille concurrentielle"]

    driver = webdriver.Chrome()

    try:
        for nom, url, ligne in produits:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".price p"), "€")
                )
                element = driver.find_element(By.CSS_SELECTOR, ".price p")


                prix = element.get_attribute("textContent")
               
                prix = re.search(r"(\d+[.,]\d+)", prix)
                prix = float(prix.group(1).replace(",", "."))
                print(prix)
                feuille.cell(row=ligne, column=3).value = prix
                

                print(nom, ":", prix, "€")
               
            except Exception:
                print(nom, ": prix introuvable, ancien prix conservé")

    finally:
        driver.quit()

    classeur.save(os.path.join(path_projet, "Book.xlsx"))
    print("Fichier Excel mis à jour !")


if __name__ == "__main__":
    take_oscaro_data()