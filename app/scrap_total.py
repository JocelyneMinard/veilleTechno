import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime
import time

# Liste structurée des pièces multi-fournisseurs
PRODUITS = [
    # --- 1. Filtre à huile PURFLUX (LS280A) ---
    {
        "fournisseur": "Oscaro", 
        "ref": "LS280A", 
        "nom": "Filtre à huile PURFLUX", 
        "url": "https://www.oscaro.com/filtre-a-huile-purflux-ls280a-1213708-7-p#/?vid=11408"
    },
    {
        "fournisseur": "Auto-Doc", 
        "ref": "LS280A", 
        "nom": "Filtre à huile PURFLUX", 
        "url": "https://www.auto-doc.fr/purflux/7852205?search=PURFLUX+Filtre+%C3%A0+huile+%28LS280A%29"
    },
    {
        "fournisseur": "Mister-Auto", 
        "ref": "LS280A", 
        "nom": "Filtre à huile PURFLUX", 
        "url": "https://www.mister-auto.com/filtre-a-huile-purflux-038-ls280a-p/"
    },

    # --- 2. Amortisseur TRW (JHT264T) ---
    {
        "fournisseur": "Oscaro", 
        "ref": "JHT264T", 
        "nom": "Amortisseur arrière TRW", 
        "url": "https://www.oscaro.com/jeu-de-2-amortisseurs-trw-jht264t-1857387-3539-p#/?vid=11408"
    },
    {
        "fournisseur": "Auto-Doc", 
        "ref": "JHT264T", 
        "nom": "Amortisseur arrière TRW", 
        "url": "https://www.auto-doc.fr/trw/2199141?search=TRW+Amortisseur+%28JHT264T%29"
    },
    {
        "fournisseur": "Mister-Auto", 
        "ref": "JHT264T", 
        "nom": "Amortisseur arrière TRW", 
        "url": "https://www.mister-auto.com/amortisseur-arriere-trw-161-jht264t-p/"
    },

    # --- 3. Plaquettes de frein VALEO (301007) ---
    {
        "fournisseur": "Oscaro", 
        "ref": "301007", 
        "nom": "Plaquettes de frein VALEO", 
        "url": "https://www.oscaro.com/jeu-de-4-plaquettes-de-frein-valeo-301007-6042068-402-p#/?vid=11408"
    },
    {
        "fournisseur": "Auto-Doc", 
        "ref": "301007", 
        "nom": "Plaquettes de frein VALEO", 
        "url": "https://www.auto-doc.fr/valeo/7949921?search=VALEO+Plaquettes+de+frein+%28301007%29"
    },
    {
        "fournisseur": "Mister-Auto", 
        "ref": "301007", 
        "nom": "Plaquettes de frein VALEO", 
        "url": "https://www.mister-auto.com/plaquette-de-frein-arriere-valeo-021-301007-p/"
    }
]

DB_NAME = "comparatif_pieces.db"

def initialiser_base_de_donnees():
    """Crée une table adaptée au comparatif multi-fournisseurs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comparatif_prix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur TEXT,
            reference TEXT,
            nom_produit TEXT,
            prix TEXT,
            url TEXT,
            statut TEXT,
            date_scraping TEXT
        )
    ''')
    conn.commit()
    conn.close()

def sauvegarder_dans_bd(donnees):
    """Enregistre le relevé d'un fournisseur dans SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_du_jour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO comparatif_prix (fournisseur, reference, nom_produit, prix, url, statut, date_scraping)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        donnees.get("fournisseur"),
        donnees.get("reference"),
        donnees.get("nom"),
        donnees.get("prix"),
        donnees.get("url"),
        donnees.get("statut"),
        date_du_jour
    ))
    conn.commit()
    conn.close()

def chercher_prix_json(data):
    """Recherche récursive d'un prix dans les données structurées JSON-LD."""
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
            if offres.get("lowPrice") is not None:
                return offres["lowPrice"]
        elif isinstance(offres, list):
            for offre in offres:
                prix = chercher_prix_json({"offers": offre})
                if prix is not None:
                    return prix
        for valeur in data.values():
            prix = chercher_prix_json(valeur)
            if prix is not None:
                return prix
    return None

def scraper_produit(driver, produit):
    fournisseur = produit["fournisseur"]
    reference = produit["ref"]
    url = produit["url"]
    
    try:
        print(f"\n🔍 [{fournisseur}] Scraping de la référence {reference}...")
        driver.get(url)
        
        # Pause d'adaptation
        time.sleep(5)
        
        # 🍪 Tentative de fermeture automatique des bannières de cookies courantes
        try:
            bouton_accept = driver.find_element("css selector", "#didomi-notice-agree-button, .cookie-accept, button[data-cky-tag='accept-all']")
            bouton_accept.click()
            time.sleep(1)
        except:
            pass # S'il n'y a pas de bandeau, on continue normalement
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Récupération du nom de la page
        nom = produit["nom"]
        titre = soup.select_one("h1")
        if titre:
            nom = titre.get_text(" ", strip=True)
            
        prix = None
        
        # 1. Recherche par balise itemprop="price"
        element_prix = soup.select_one('[itemprop="price"]')
        if element_prix:
            prix = element_prix.get("content") or element_prix.get_text(strip=True)
        
        # 2. Recherche par balise Meta OpenGraph
        if prix is None:
            meta_prix = soup.select_one('meta[property="product:price:amount"]')
            if meta_prix:
                prix = meta_prix.get("content")
        
        # 3. Recherche par les scripts JSON-LD
        if prix is None:
            scripts = soup.select('script[type="application/ld+json"]')
            for script in scripts:
                try:
                    data = json.loads(script.string or script.get_text())
                    prix = chercher_prix_json(data)
                    if prix is not None:
                        break
                except (json.JSONDecodeError, TypeError):
                    continue
        
        # 4. Sélecteurs de secours génériques
        if prix is None:
            element_fallback = soup.select_one(".price_item, .product_price-value, .price, .product-price")
            if element_fallback:
                prix = element_fallback.get_text(strip=True)

        if prix is None:
            print(f"❌ Prix introuvable chez {fournisseur} pour la réf {reference}.")
            return {
                "fournisseur": fournisseur,
                "reference": reference,
                "nom": nom,
                "prix": None,
                "url": url,
                "statut": "Prix introuvable"
            }

        print(f"✅ [{fournisseur}] Prix trouvé : {prix}")
        return {
            "fournisseur": fournisseur,
            "reference": reference,
            "nom": nom,
            "prix": str(prix).strip(),
            "url": url,
            "statut": "Succès"
        }

    except Exception as e:
        print(f"❌ Erreur critique sur {url} : {str(e)}")
        return {
            "fournisseur": fournisseur,
            "reference": reference,
            "nom": produit["nom"],
            "prix": None,
            "url": url,
            "statut": f"Échec : {str(e)}"
        }
def lancer_comparatif():
    initialiser_base_de_donnees()
    
    driver = None
    try:
        print("🚀 Lancement du navigateur de veille concurrentielle...")
        driver = uc.Chrome(version_main=156, use_subprocess=True)  # Ajustez version_main selon votre Chrome
        driver.maximize_window()

        for produit in PRODUITS:
            resultat = scraper_produit(driver, produit)
            sauvegarder_dans_bd(resultat)
            
            print(json.dumps(resultat, indent=4, ensure_ascii=False))
            print("-" * 60)
            
            # Pause de courtoisie entre chaque requête pour éviter d'être bloqué
            time.sleep(3)

    finally:
        if driver:
            driver.quit()
        print("\n✨ Veille concurrentielle multi-fournisseurs terminée ! Données stockées dans 'comparatif_pieces.db'.")

if __name__ == "__main__":
    lancer_comparatif()