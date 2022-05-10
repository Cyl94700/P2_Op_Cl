"""
                                    Script niveau catégorie :
                    Récuprère les URL de chacune des pages de la catégorie Mystery
                    Récuprère les URL des 32 livres de la catégorie
                    Récuprère les 10 informations désirées de chaque livre de la catégorie
                    Ecrit dans un csv nommé "Mystery" à l'intérieur d'un dossier "csv_files"
                    Récupère les images des livres dans un dossier nommé "Mystery" à l'intérieur
                    d'un dossier "images.jpg" si elles n'existent pas déjà
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

# Initialisation de l'url sur la catégorie mystery qui comporte 2 pages et 32 livres :
url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html'

# Si Page trouvée, on parse la page avec BeautifulSoup
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')

# détermination du nombre de pages de la catégorie avec la fonction "number_page_category"
number_page = number_page_category(soup)

# Création de la liste des liens url d'une catégorie
link = url
i = 0
book_links = []
if number_page > 1:
    # Pour chaque page on récupère les url des livres dans une liste
    for n in range(1, number_page + 1):
        # On met en forme l'url de la page n
        if n > 1:
            i = n - 1
        link = link.replace("page-" + str(i), "page-" + str(n))
        response = requests.get(link)
        if response.ok:
            # Récupération objet BeautifulSoup de la page
            soup = BeautifulSoup(response.text, 'html.parser')
            # Récupération des url (livres) d'une page de catégorie avec la focntion links_book_category
            book_links = links_book_category(soup, book_links)
else:
    # On récupère les url des livres de l'unique page
    book_links = links_book_category(soup, book_links)

# Memorisation des "10 données livre" de tous les livres d'une catégorie" avec la fonction data_book
data_books_category = []
for book_link in book_links:
    data_book_one = data_book(book_link)
    data_books_category.append(data_book_one)

# Eciture csv de tous les livres d'une catégorie

en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
           "price_excluding_tax", "number_available", "product_description", "category",
           "review_rating", "image_url"]

# Création/Ecriture dans fichier csv de tous les livres de la catégorie Mystery "Mystery.csv" :

with open(data_book_one[7] + '.csv', "w", encoding="utf-8-sig", newline='') as fichier_csv:

    # Création objet writer
    writer = csv.writer(fichier_csv, delimiter=';', dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
    # ecriture en tête
    writer.writerow(en_tete)
    # Ecriture ligne detail à partir de la liste data_books_category
    for data_line in data_books_category:
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
        # On télécharge l'image si elle n'existe pas
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
            # navigation vers dossier "csv_file"
            folder = folder.replace('\\images.jpg\\' + (data_line[7]), '' + "\\csv_files")
            folder_navigation(folder)

# Message extraction_page terminée
print("extraction terminée")
