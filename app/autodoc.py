from playwright.sync_api import sync_playwright

def obtenir_donnees_autodoc():
    url = "https://www.auto-doc.fr/valeo/7949921?search=VALEO+Plaquettes+de+frein+%28301007%29"
    
    with sync_playwright() as p:
        # Lancement du navigateur (headless=False permet de voir le navigateur s'ouvrir à l'écran, idéal pour étudier)
        browser = p.chromium.launch(headless=True)
        
        # Création d'un contexte avec un User-Agent réaliste
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = context.new_page()
        
        try:
            print(f"Connexion en cours vers : {url}")
            # Navigation vers la page (timeout de 60 secondes)
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            
            # Petite pause pour laisser le temps aux scripts de protection/Cloudflare de valider la session (si nécessaire)
            page.wait_for_timeout(3000)
            
            # --- RECHERCHE DU PRIX ---
        
            # Note : Les sélecteurs CSS changent souvent. 
            # On cherche un sélecteur large ou on utilise une classe fréquente sur le site.
            # En cours d'étude, n'hésitez pas à inspecter la page pour ajuster ce sélecteur.
            selecteur_prix = ".price, .product_price, [data-qa='product-price']"
            
            # On attend que l'élément apparaisse (max 10 secondes)
            page.wait_for_selector(selecteur_prix, timeout=10000)
            
            prix_element = page.locator(selecteur_prix).first
            
            if prix_element.count() > 0:
                prix_texte = prix_element.inner_text().strip()
                print(f"Succès ! Prix trouvé : {prix_texte}")
                return {
                    "statut": "Succès",
                    "url": url,
                    "prix": prix_texte
                }
            else:
                print("Élément introuvable avec les sélecteurs actuels.")
                # Sauvegarde d'une capture d'écran pour analyser visuellement le résultat
                page.screenshot(path="debug_capture.png")
                return {"statut": "Échec", "erreur": "Sélecteur introuvable (voir debug_capture.png)"}
                
        except Exception as e:
            print( une_erreur := f"Une erreur est survenue : {str(e)}")
            # En cas de blocage Cloudflare ou autre, une capture aide à comprendre
            try:
                page.screenshot(path="erreur_capture.png")
            except:
                pass
            return {"statut": "Bloqué ou Erreur", "erreur": str(e)}
            
        finally:
            browser.close()

# Exécution du script
resultat = obtenir_donnees_autodoc()
print("\nRésultat final de la fonction :", resultat)