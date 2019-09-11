from django.core.management.base import BaseCommand, CommandError
from library.models import ProductCategorie, Product
import math
import requests as rq


class Command(BaseCommand):
    help = 'Import datas from api OFF'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Démarrage de la mise à jour...")

        off_cat = 'https://fr.openfoodfacts.org/categories.json'

        def get_data_api(url):
            """" Get all data from api OpenFoodFacts """

            data = rq.get(url)
            return data.json()

        def categories_table(url):
            """ Get category from json data of openfoodfacts and insert in table categories"""

            get_data = get_data_api(url)
            for data in get_data["tags"]:

                if data["products"] in range(55, 60) and 'en:' in data['id']:
                    category = ProductCategorie.objects.create(name_category=data["name"], link_category=data["url"])
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
                        fat_100g = product["nutriments"]["fat_100g"]
                    except KeyError:
                        fat_100g = "N/A"

                    try:
                        sugars_100g = product["nutriments"]["sugars_100g"]
                    except KeyError:
                        sugars_100g = "N/A"

                    try:
                        saturated_fat_100g = product["nutriments"]["saturated-fat_100g"]
                    except KeyError:
                        saturated_fat_100g = "N/A"

                    try:
                        salt_100g = product["nutriments"]["salt_100g"]
                    except KeyError:
                        salt_100g = "N/A"

                    try:
                        product_nutriscore = product["nutrition_grade_fr"]

                    except KeyError:
                        product_nutriscore = "e"

                    try:
                        product_link = product["url"]
                    except KeyError:
                        product_link = "N/A"

                    try:
                        product_img = product["image_front_url"]
                    except KeyError:
                        product_img = ""

                    try:
                        product = Product.objects.create(
                            name_product=product_mane,
                            categorie_id=id_categories,
                            nutriscore_product=product_nutriscore,
                            fat_100g=fat_100g,
                            sugars_100g=sugars_100g,
                            saturated_fat_100g=saturated_fat_100g,
                            salt_100g=salt_100g,
                            image_product=product_img,
                            link_product=product_link,
                        )

                        product.save()

                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this product: {}\n{}".format(product_mane, str(ex))
                        print(msg)

        categories_table(off_cat)
        categories_product = ProductCategorie.objects.all()

        for data in categories_product:
            id_cate = data.id
            link_cate = data.link_category
            products_table(id_cate, link_cate)
