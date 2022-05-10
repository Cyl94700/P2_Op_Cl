# Importation des packages necessaires
import requests
from bs4 import BeautifulSoup
import csv

# Initialisation de la constante URL racine
URL_INDEX = 'http://books.toscrape.com/'

# Adresse url initialisée sur le premier livre de la catégorie History :
url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'
page = requests.get(url)

# On "parse" la page avec BeautifulSoup si acces ok
if page.ok:
    soup = BeautifulSoup(page.content, 'html.parser')

# Récupération des éléments :

    product_page_url = url
    universal_product_code = soup.find_all('td')[0].get_text()
    title = soup.find("h1").string
    price_including_tax = soup.find_all('td')[3].get_text()
    price_including_tax = price_including_tax.replace('.', ',')
    price_excluding_tax = soup.find_all('td')[2].get_text()
    price_excluding_tax = price_excluding_tax.replace('.', ',')
    number_available_string = soup.find_all('td')[5].get_text()
    number_available = (number_available_string.split(' ')[2].replace('(', ''))
    product_description = soup.find_all('p')[3].get_text()
    category = soup.find_all('a')[3].get_text()
    stars = str(soup.select(".star-rating")[0])
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
    review_rating = rating
    image_url = soup.find_all('img')[0]
    image_url = URL_INDEX + image_url['src'].replace("../", '')

# Ecriture fichier csv :

    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category",
               "review_rating", "image_url"]

    with open('data.csv', 'w', encoding="utf-8-sig", newline='') as fichier_csv:

        # Création objet writer (écriture) avec ce fichier

        writer = csv.writer(fichier_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writerow(en_tete)

        ligne = [product_page_url, universal_product_code, title, price_including_tax,
                 price_excluding_tax, number_available, product_description, category,
                 review_rating, image_url]

        writer.writerow(ligne)
