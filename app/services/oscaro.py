import os
import random
import re
import sys
import time
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver


def take_oscaro_data():
    path_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    if path_projet not in sys.path:
        sys.path.insert(0, path_projet)

    produits = [
        (
            "Filtre à huile Purflux",
            "https://www.oscaro.com/filtre-a-huile-purflux-ls280a-1213708-7-p",
            2,
        ),
        (
            "Amortisseur TRW",
            "https://www.oscaro.com/jeu-de-2-amortisseurs-trw-jht264t-1857387-3539-p",
            3,
        ),
        (
            "Plaquettes Valeo",
            "https://www.oscaro.com/jeu-de-4-plaquettes-de-frein-valeo-301007-6042068-402-p",
            4,
        ),
    ]

    classeur = load_workbook(os.path.join(path_projet, "Book.xlsx"))
    feuille = classeur["Veille concurrentielle"]

    # Initialise Chrome en mode furtif (Undetected Chromedriver)
    driver = Driver(uc=True)

    try:
        for nom, url, ligne in produits:
            try:
                # Ouvre l'URL en déconnectant brièvement le pilote pour passer Cloudflare
                driver.uc_open_with_reconnect(url.strip(), reconnect_time=5)

                WebDriverWait(driver, 30).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".price p"), "€")
                )
                element = driver.find_element(By.CSS_SELECTOR, ".price p")

                texte_prix = element.get_attribute("textContent")
                match = re.search(r"(\d+[.,]\d+)", texte_prix)

                if match:
                    prix = float(match.group(1).replace(",", "."))
                    feuille.cell(row=ligne, column=3).value = prix
                    print(f"{nom} : {prix} €")

                # Pause naturelle entre deux fiches produits
                time.sleep(random.uniform(3, 6))

            except Exception as e:
                print(f"{nom} : échec ({type(e).__name__})")
                driver.save_screenshot(f"erreur_{ligne}.png")

    finally:
        driver.quit()

    classeur.save(os.path.join(path_projet, "Book.xlsx"))
    print("Fichier Excel mis à jour !")


if __name__ == "__main__":
    take_oscaro_data()