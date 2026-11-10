import requests
from bs4 import BeautifulSoup

def obtenir_donnees_oscaro():
    url = "https://www.oscaro.com/jeu-de-4-plaquettes-de-frein-valeo-301007-6042068-402-p#/?vid=11408"
    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Correction 1 : On passe response.text (le code HTML reçu) à BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # --- MÉTHODE 1 : Le Sélecteur CSS ---
            prix_element = soup.select_one(".price p")
            prix_propre_1 = "Non trouvé"
            if prix_element:
                prix_propre_1 = prix_element.text.strip()
                print(f"Méthode 1 - Prix trouvé : {prix_propre_1}")

            # --- MÉTHODE 2 : Le chaînage avec .find() ---
            bloc_parent = soup.find("div", class_="price")
            prix_propre_2 = "Non trouvé"
            if bloc_parent:
                sous_element_prix = bloc_parent.find("p")
                if sous_element_prix:
                    prix_propre_2 = sous_element_prix.text.strip()
                    print(f"Méthode 2 - Prix trouvé : {prix_propre_2}")
            
            # On renvoie un dictionnaire exploitable par Flask
            return {
                "statut": "Succès",
                "prix_methode_1": prix_propre_1,
                "prix_methode_2": prix_propre_2
            }
        else:
            return {"erreur": f"Code statut {response.status_code}", "statut": "Échec"}
            
    except Exception as e:
        return {"erreur": str(e), "statut": "Bloqué ou Erreur"}

# Exécution du script
resultat = obtenir_donnees_oscaro()
print("\nRésultat final de la fonction :", resultat)