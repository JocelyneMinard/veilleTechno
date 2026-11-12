# Projet veille technoloique

# Technique
Afin de valider la théorie du scraping, nous avons cherché à réaliser un test.
Au départ, nous avons essayé de récupérer les données en JSON, mais les sites automobiles repèrent que nous arrivons d'un script Python et cela peu importe si nous utilisons Request ou CloudScraper. Nous avons donc essayé avec Selenium.

## Excel
Nous avons utilisé un fichier Excel pour comparer nos prix avec ceux des trois concurrents : Oscaro, AutoDoc et Mister-Auto.

Pour calculé justement cette écart de prix nous avons utilisé la formule suivant :

=SI(OU(C6="";NB(D6:F6)=0);"";C6-MIN(D6:F6))

Cette formule veut dire que la fonction SI associée à OU permet de vérifié si un prix est manquant. Si tous les prix sont présents,
la formule calcule la différence entre notre prix et celui du concurrent le moins chère. Sinon, la cellule restera vide.

Les prix récupérés par nos codes fait en python sont ensuite enregistrés automatiquement dans le fichier Excel.

## Flask
Nous sommes passés par flak pour avoir un site afin de lancer les scripts de scraping et afficher le tableau Excel. Ce mini-POC teste seulement la faisabilité du scraping sur les sites concurrents
La technologie pour faire cela est Selenium. Il utilise une session Chrome afin d'ouvrir les URL pour récupérer les prix
Le POC n'est qu'une première étape de scraping car pour le moment cela est très lourd pour seulement 3 produits, des optimisations sont à réaliser

## Stockage
Le POC se base sur un fichier Excel, pour plus de robustesse il faudra une base de données SQLite ou PostgreSQL


