"""
                            Script niveau toutes catégories :
                    Récuprère les URL de chacune des 50 catégories
                    Récuprère les URL de chacune des pages d'une catégorie
                    Récuprère les URL de chacun des livres d'une catégorie
                    Récuprère les 10 informations désirées de chaque livre
                    Ecrit dans un csv ces informations par catégorie
                    Récupère les images des livres par catégorie si elles n'existent pas déjà
"""
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from functions import data_book, number_page_category, links_book_category, folder_navigation,\
     download_image, short_image_title

# Création du dossier "csv_files" ou navigation vers celui-ci (fonction folder_navigation)
folder = "csv_files"
folder_navigation(folder)

# Construction de la liste des catégories à partir de la page d'accueil du site
url_site = "http://books.toscrape.com/index.html"


# Si Page trouvée, on parse la page avec BeautifulSoup
response = requests.get(url_site)
if response.ok:
    # On prépare pour analyse
    soup_index = BeautifulSoup(response.text, 'html.parser')
    links_list = soup_index.find('ul', {'class': "nav nav-list"}).find('ul').find_all('li')
    # On boucle sur toutes les catégories
    for li in links_list:
        a = li.find('a')
        cat = a.get_text().strip()
        url_cat = 'http://books.toscrape.com/' + a['href']
        print("\n")
        print(cat)

        # détermination du nombre de pages de la catégorie avec la fonction "number_page_category"
        response = requests.get(url_cat)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            number_page = number_page_category(soup)

            # Création de la liste des liens url d'une catégorie
            link = url_cat
            # i = 0
            book_links = []
            if number_page > 1:
                # Pour chaque page on récupère les url des livres dans une liste
                for n in range(1, number_page + 1):
                    # On met en forme l'url de la page n
                    if n > 1:
                        link = link.replace("index.html", '') + "page-" + str(n) + ".html"
                        response = requests.get(link)
                    if response.ok:
                        # Récupération objet BeautifulSoup de la page
                        soup_p = BeautifulSoup(response.text, 'html.parser')
                        # Récupération des url (livres) d'une page de catégorie avec la focntion links_book_category
                        book_links = links_book_category(soup_p, book_links)
            else:
                # on parse la page unique de la catégorie
                response = requests.get(link)
                # Récupération objet BeautifulSoup de la page
                soup_p = BeautifulSoup(response.text, 'html.parser')
                # On récupère en liste les url des livres de l'unique page
                book_links = links_book_category(soup_p, book_links)

            # Memorisation des "10 données livre" de tous les livres d'une catégorie avec la fonction data_book

            data_books_category = []
            for book_link in book_links:
                data_book_one = data_book(book_link)
                data_books_category.append(data_book_one)

            # Eciture csv de tous les livres d'une catégorie

            en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                       "price_excluding_tax", "number_available", "product_description", "category",
                       "review_rating", "image_url"]

            # Création/Ecriture nouveau fichier appelé « "catégorie".csv »

            with open(data_book_one[7] + '.csv', "w", encoding="utf-8-sig", newline='') as fichier_csv:
                # Création objet writer
                writer = csv.writer(fichier_csv, delimiter=';', dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
                # ecriture en tête
                writer.writerow(en_tete)
                # On boucle sur la liste des livres par catégorie
                for data_line in data_books_category:
                    # Ecriture ligne détail
                    writer.writerow(data_line)
                    # récupération directory
                    folder = os.getcwd()
                    # navigation vers dossier parent
                    folder = folder.replace('\\csv_files', '')
                    folder_navigation(folder)
                    # Création du dossier image.jpg ou navigation vers celui-ci
                    folder = folder + "\\images.jpg"
                    folder_navigation(folder)
                    # Création du dossier "catégorie" ou navigation vers celui-ci
                    folder = folder + "\\" + data_line[7]
                    folder_navigation(folder)
                    # Mise en forme d'un titre court pour le nom de l'image
                    image_title = data_line[2]
                    image_title = short_image_title(image_title)
                    # Premier paramètre de la fonction download_image
                    image_title = image_title + '.jpg'
                    # Deuxième paramètre de la fonction download_image
                    image_url = data_line[9]
                    # On télécharge l'image si elle n'existe pas.
                    try:
                        with open(image_title, "rb"):
                            pass
                            # récupération directory
                            folder = os.getcwd()
                            # navigation vers dossier parent
                            folder = folder.replace('\\images.jpg\\' + data_line[7], '' + "\\csv_files")
                            folder_navigation(folder)
                    except FileNotFoundError:
                        download_image(image_url, image_title)
                        time.sleep(0.5)
                        # récupération directory
                        folder = os.getcwd()
                        # # navigation vers dossier "csv_file"
                        folder = folder.replace('\\images.jpg\\' + (data_line[7]), '' + "\\csv_files")
                        folder_navigation(folder)

# Message extraction_page terminée
print("extraction terminée")
