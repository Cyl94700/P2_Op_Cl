*****************************************
**OpenClassrooms: Projet 2: Books To Scrape**
*****************************************
**Description :**

Ce script récupère 10 informations différentes pour chacun des 1OOO livres du  site http://books.toscrape.com/ :

•	product_page_url

•	Universal Product Code (upc)

•	title

•	price_including_tax

•	price_excluding_tax

•	number_available

•	product_description

•	category

•	review_rating

•	image_url

Ces informations sont stockées dans des fichiers csv correspondant à chaque catégorie de livres(Catégorie.csv).
Les images sont stockées dans des dossiers csv correspondant à chaque catégorie de livres(Catégorie)
*************************************************************************************************************

**Installation :**

**Création et activation d’un environnement virtuel :**

•	Depuis le terminal, lancer la commande :

`python -m venv env`

•	Activer l’environnement :  

Sur windows:

`env/Scripts/activate`

Sur mac ou linux:   

`source env/bin/activate` 
                              
**Installation des packages nécessaires depuis le fichier requirements.txt :**

•	Lancer la commande  :    

`pip install -r requirements.txt`
`

**Exécution :**

•Lancer la commande : 

`python all_categories.py`
