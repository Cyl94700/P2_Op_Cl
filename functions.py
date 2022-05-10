import requests
import bs4
from bs4 import BeautifulSoup
import os

# Initialisation de la constante URL racine
URL_INDEX = 'http://books.toscrape.com/'
"""
                            FONCTIONS APPELEES PAR LE PGM PRINCIPAL
"""

"""  
 Fonction data_book de récupération des 10 informations demandées sur une page  
 Paramètres :  
 En entrée => url d'un livre
 En sortie => liste data_book_one des 10 informations 
"""


def data_book(book_link):
    product_page_url = book_link
    page = requests.get(book_link)
    soup_p = BeautifulSoup(page.content, 'html.parser')
    universal_product_code = soup_p.find_all('td')[0].get_text()
    title = soup_p.find("h1").string
    print(title)
    price_including_tax = soup_p.find_all('td')[3].get_text()
    price_including_tax = price_including_tax.replace('.', ',')
    price_excluding_tax = soup_p.find_all('td')[2].get_text()
    price_excluding_tax = price_excluding_tax.replace('.', ',')
    number_available_string = soup_p.find_all('td')[5].get_text()
    number_available = (number_available_string.split(' ')[2].replace('(', ''))
    product_description = soup_p.find_all('p')[3].get_text()
    category = soup_p.find_all('a')[3].get_text()
    stars = str(soup_p.select(".star-rating")[0])
    offset = stars.find("star-rating")
    stars = stars[offset:offset + 15]
    rating = 0
    if "One" in stars:
        rating = 1
    elif "Two" in stars:
        rating = 2
    elif "Thr" in stars:
        rating = 3
    elif "Fou" in stars:
        rating = 4
    elif "Fiv" in stars:
        rating = 5
    review_rating = str(rating)
    image_url = soup_p.find_all('img')[0]
    image_url = URL_INDEX + image_url['src'].replace("../", '')

    # mémorisation de toutes les données "livre" d'une page de catégorie"
    data_book_one = [product_page_url, universal_product_code, title,
                     price_including_tax, price_excluding_tax, number_available,
                     product_description, category, review_rating, image_url]
    return data_book_one


"""  
 Fonction number_page_book : détermine le nombre de page d'une catégorie  
 Paramètres :  
 En entrée => soup : objet BeautifulSoup de la première page d'une catégorie
 En sortie => nb_page : entier corresepondant au nombre de pages de la catégorie
"""


def number_page_category(soup):

    # Recherche classe "plusieurs pages" :
    nb_page = soup.find("li", {"class": "current"})
    # Si plusieurs pages, nb_page = type bs4.element.Tag
    if isinstance(nb_page, bs4.element.Tag):
        # On récupère le nombre de pages
        nb_page = int(nb_page.get_text().strip()[-1])
    else:
        nb_page = 1
    return nb_page


"""  
 Fonction links_book_category : construit tous les liens url "livre" d'une catégorie 
 Paramètres :  
 En entrée => soup_p : objet BeautifulSoup de la page d'une catégorie
 En sortie => liste links   
"""


def links_book_category(soup_p, liste_cat):

    # Recherche des url de chaque livre
    book_links = soup_p.find_all("div", {'class': 'image_container'})
    # Pour chaque livre on rajoute l'url du livre à la liste des url de cette catégorie
    # book_links = []
    for div in book_links:
        a = div.find('a')
        liste_cat.append('http://books.toscrape.com/catalogue/' + a['href'].replace("../", ''))

    return liste_cat


"""
 Fonction write_book d'écriture d'une ligne detail dans le fichier csv  
 Paramètre :  
 En entrée => liste data_book_page_categorie
"""


def folder_navigation(folder):
    """
    Cette fonction permet la navigation vers un dossier
    Si le dossier n'existe pas encore il est créé.
    """
    # try navigation vers dossier de sauvegarde
    try:
        os.chdir(folder)
    # si échec créer dossier puis navigation
    except FileNotFoundError:
        os.mkdir(folder)
        os.chdir(folder)


def download_image(img_url, image_title):
    f = open(image_title, 'wb')
    response = requests.get(img_url)
    f.write(response.content)
    f.close()


def short_image_title(image_title):
    """
    Cette fonction raccourcit et nettoie le titre du livre de caractères interdits
    pour servir de nom au fichier image téléchargé
    En entrée : image_title
    En sortie : short_title
    """
    # Liste de caractères indésirables
    characters_filter = [',', ';', '’', '/', '\\',
                         ':', '*', '?', '"', '<', '>', '|']
    for character in characters_filter:
        image_title = image_title.replace(character, '')  # Nettoyage du titre
    title_list = image_title.split()
    # Détermine le nombre de mots du nom de l'image
    if len(title_list) > 10:
        nb_words_title_img = 5
    else:
        nb_words_title_img = len(title_list)
    # Reconstruit un titre avec maximum les 5 premiers mots et des underscores
    image_title = "_".join(title_list[:nb_words_title_img])
    return image_title
