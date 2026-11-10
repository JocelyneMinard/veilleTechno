from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import load_workbook

produits = [
    ("Filtre à huile Purflux", "https://www.mister-auto.com/filtre-a-huile-purflux-038-ls280a-p/", 6),
    ("Amortisseur TRW", "https://www.mister-auto.com/amortisseur-arriere-trw-161-jht264t-p/", 7),
    ("Plaquettes Valeo", "https://www.mister-auto.com/plaquette-de-frein-arriere-valeo-021-301007-p/", 8)
]

classeur = load_workbook("Book.xlsx")
feuille = classeur["Veille concurrentielle"]

driver = webdriver.Chrome()

try:
    for nom, url, ligne in produits:
        try:
            driver.get(url)

            element = driver.find_element(By.CSS_SELECTOR, ".large-price--std")

            prix = element.get_attribute("textContent")
            prix = float(prix.replace("€", "").replace("\xa0", "").replace(",", ".").strip())

            feuille.cell(row=ligne, column=6).value = prix

            print(nom, ":", prix, "€")

        except Exception:
            print(nom, ": prix introuvable, ancien prix conservé")

finally:
    driver.quit()

classeur.save("Book.xlsx")
print("Fichier Excel mis à jour !")
