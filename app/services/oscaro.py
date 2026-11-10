from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json


URL = "https://www.oscaro.com/jeu-de-4-plaquettes-de-frein-valeo-301007-6042068-402-p#/?vid=11408"


def chercher_prix_json(data):
    """Recherche un prix dans les données JSON-LD."""
    if isinstance(data, list):
        for element in data:
            prix = chercher_prix_json(element)
            if prix is not None:
                return prix

    elif isinstance(data, dict):
        offres = data.get("offers")

        if isinstance(offres, dict):
            if offres.get("price") is not None:
                return offres["price"]

        elif isinstance(offres, list):
            for offre in offres:
                prix = chercher_prix_json(
                    {"offers": offre}
                )
                if prix is not None:
                    return prix

        for valeur in data.values():
            prix = chercher_prix_json(valeur)
            if prix is not None:
                return prix

    return None


def obtenir_donnees_oscaro():
    driver = None

    try:
        
        options = Options()
        options.add_argument("--start-maximized")

        print("Ouverture de Google Chrome...")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)

        
        driver.get(URL)

        print("Page ouverte :", driver.current_url)

        
        input(
            "Quand la page est chargée, "
            "appuie sur Entrée dans le terminal..."
        )

        
        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        
        print("Titre de la page :", driver.title)

        
        nom = "Plaquettes de frein arrière VALEO"

        titre = soup.select_one("h1")

        if titre:
            nom = titre.get_text(" ", strip=True)

        
        prix = None

        
        element_prix = soup.select_one(
            '[itemprop="price"]'
        )

        if element_prix:
            prix = (
                element_prix.get("content")
                or element_prix.get_text(strip=True)
            )

        
        if prix is None:
            meta_prix = soup.select_one(
                'meta[property="product:price:amount"]'
            )

            if meta_prix:
                prix = meta_prix.get("content")

        
        if prix is None:
            scripts = soup.select(
                'script[type="application/ld+json"]'
            )

            for script in scripts:
                try:
                    data = json.loads(
                        script.string or script.get_text()
                    )

                    prix = chercher_prix_json(data)

                    if prix is not None:
                        break

                except (json.JSONDecodeError, TypeError):
                    continue

        
        if prix is None:
            return {
                "nom": nom,
                "prix": None,
                "url": URL,
                "statut": "Prix introuvable"
            }

        return {
            "nom": nom,
            "prix": str(prix),
            "url": URL,
            "statut": "Succès"
        }

    except Exception as e:
        return {
            "erreur": str(e),
            "statut": "Échec"
        }

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    resultat = obtenir_donnees_oscaro()

    print("\n========== RÉSULTAT ==========")
    print(json.dumps(
        resultat,
        indent=4,
        ensure_ascii=False
    ))
