from django.shortcuts import render

from .models import ProductCategories, Products
from django.template import loader
from django.http import HttpResponse
import math
import requests as rq


def import_data(requests):

    off_cat = 'https://fr.openfoodfacts.org/categories.json'
    off_url = 'https://fr.openfoodfacts.org'
    nutriscore = {0: 'N/A',
                  1: 'A',
                  2: 'B',
                  3: 'C',
                  4: 'D',
                  5: 'E'
                  }

    def get_data_api(url):
        """" Get all data from api OpenFoodFacts """

        data = rq.get(url)
        return data.json()

    def categories_table(url):
        """ Get category from json data of openfoodfacts and insert in table categories"""

        get_data = get_data_api(url)
        for data in get_data["tags"]:

            if data["products"] in range(55, 60) and 'en:' in data['id']:
                category = ProductCategories.objects.create(name_category=data["name"], link_category=data["url"])
                category.save()

    def products_table(id_categories, url_categories):
        """ Get all products from categories and insert into database """

        url_json = str(''.join(url_categories))
        get_data = get_data_api(url_json + ".json")
        nb_pages = int(math.ceil(get_data["count"] / get_data["page_size"]))

        for page in range(0, nb_pages):
            categories_pages = url_json + "/" + str(page+1) + ".json"
            get_data_categories = get_data_api(categories_pages)

            for product in get_data_categories["products"]:

                try:
                    product_mane = product["product_name_fr"]
                except KeyError:
                    product_mane = "N/A"

                try:
                    product_brand = product["brands"]
                except KeyError:
                    product_brand = "N/A"

                try:
                    product_description = str(product["ingredients_text_fr"])
                except KeyError:
                    product_description = "N/A"

                try:
                    nutri_grade = product["nutrition_grade_fr"]
                    product_nutriscore = list(nutriscore.keys())[
                        list(nutriscore.values()).index(nutri_grade.upper())]

                except KeyError:
                    product_nutriscore = "5"

                try:
                    product_link = product["url"]
                except KeyError:
                    product_link = "N/A"

                try:
                    product = Products.objects.create(
                        name_product=product_mane,
                        brand_product=product_brand,
                        id_categories=id_categories,
                        description_product=product_description[:200],
                        nutriscore_product=product_nutriscore,
                        image_product="",
                        link_product=product_link,
                    )

                    product.save()

                except Exception as ex:
                    print(str(ex))
                    msg = "\n\nSomething went wrong saving this product: {}\n{}".format(product_mane, str(ex))
                    print(msg)

    categories_table(off_cat)
    categories_product = ProductCategories.objects.all()

    for data in categories_product:
        id_cate = data.id
        link_cate = data.link_category
        products_table(id_cate, link_cate)


    indr = "[Info] Dump data is ok!"
    return HttpResponse(indr)


def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)
    #template = loader.get_template('library/index.html')
    #return HttpResponse(template.render(request=request))
