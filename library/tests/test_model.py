from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from library.models import ProductCategorie, Product, UserSaveProduct


class DetailPageProduct(TestCase):
    """ Test detail page """
    def setUp(self):
        ProductCategorie.objects.create(name_category='Chocolat au Caramel',
                                        link_category='https://fr.openfoodfacts.org/categorie/chocolats-au-caramel')

        self.category = ProductCategorie.objects.get(name_category='Chocolat au Caramel')

        Product.objects.create(
            name_product='Chocalat caramel',
            categorie_id=self.category.id,
            nutriscore_product='E',
            fat_100g='30.7',
            sugars_100g='56.8',
            saturated_fat_100g='18.4',
            salt_100g='0.3',
            image_product='https://static.openfoodfacts.org/images/products/541/312/136/2639/front_fr.10.400.jpg',
            link_product='https://fr.openfoodfacts.org/produit/5413121362639/chocolat-lait-caramel-sale-fair-trade',
        )

        self.product = Product.objects.get(name_product='Chocalat caramel')

    def test_detail_product(self):
        product_id = self.product.id

        response = self.client.get(reverse('detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_product_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class LoginUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

    def test_login_user(self):
        client = Client()
        response = client.post('/library/login/', {'username': 'Test', 'password': 'testdjango'})
        self.assertEqual(response.status_code, 200)
        response = client.get('/library/profile/')
        self.assertContains(response, 'Test')


class RegisterUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

    def test_register_user(self):
        client = Client()
        response = client.post('/library/register/', {'username': 'Test', 'password': 'testdjango', 'email': 'test@django.fr'})
        self.assertEqual(response.status_code, 200)
        response = client.post('/library/login/', {'username': 'Test', 'password': 'testdjango'})
        self.assertEqual(response.status_code, 200)
        response = client.get('/library/profile/')
        self.assertContains(response, 'Test')


class SaveTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

        ProductCategorie.objects.create(name_category='Chocolat au Caramel',
                                        link_category='https://fr.openfoodfacts.org/categorie/chocolats-au-caramel')

        self.category = ProductCategorie.objects.get(name_category='Chocolat au Caramel')

        Product.objects.create(
            name_product='Chocalat caramel',
            categorie_id=self.category.id,
            nutriscore_product='E',
            fat_100g='30.7',
            sugars_100g='56.8',
            saturated_fat_100g='18.4',
            salt_100g='0.3',
            image_product='https://static.openfoodfacts.org/images/products/541/312/136/2639/front_fr.10.400.jpg',
            link_product='https://fr.openfoodfacts.org/produit/5413121362639/chocolat-lait-caramel-sale-fair-trade',
        )

        self.product = Product.objects.get(name_product='Chocalat caramel')

    def test_save(self):
        client = Client()
        client.login(username="Test", password="testdjango")
        old_count = UserSaveProduct.objects.filter(user_id=self.user.id).count()
        response = client.post(
            '/library/save/?id=' + str(self.product.id),
            {
                'user_id': self.user.id,
                'product_id': self.product.id
            }
        )
        new_count = UserSaveProduct.objects.filter(user_id=self.user.id).count()
        self.assertEqual(new_count, old_count + 1)
        assert response.status_code == 200


class SearchTestCase(TestCase):
    def setUp(self):
        ProductCategorie.objects.create(name_category='Chocolat au Caramel',
                                        link_category='https://fr.openfoodfacts.org/categorie/chocolats-au-caramel')

        self.category = ProductCategorie.objects.get(name_category='Chocolat au Caramel')

        Product.objects.create(
            name_product='Chocalat caramel',
            categorie_id=self.category.id,
            nutriscore_product='E',
            fat_100g='30.7',
            sugars_100g='56.8',
            saturated_fat_100g='18.4',
            salt_100g='0.3',
            image_product='https://static.openfoodfacts.org/images/products/541/312/136/2639/front_fr.10.400.jpg',
            link_product='https://fr.openfoodfacts.org/produit/5413121362639/chocolat-lait-caramel-sale-fair-trade',
        )

    def test_search(self):
        client = Client()
        products = Product.objects.filter(name_product__icontains='chocolat')
        response = client.post(
            '/library/search/?query=' + str(products),
            {
                'products': products
            }
        )
        self.assertNumQueries(1)
        assert response.status_code == 200


class SavedProductsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

        ProductCategorie.objects.create(name_category='Chocolat au Caramel',
                                        link_category='https://fr.openfoodfacts.org/categorie/chocolats-au-caramel')

        self.category = ProductCategorie.objects.get(name_category='Chocolat au Caramel')

        Product.objects.create(
            name_product='Chocalat caramel',
            categorie_id=self.category.id,
            nutriscore_product='E',
            fat_100g='30.7',
            sugars_100g='56.8',
            saturated_fat_100g='18.4',
            salt_100g='0.3',
            image_product='https://static.openfoodfacts.org/images/products/541/312/136/2639/front_fr.10.400.jpg',
            link_product='https://fr.openfoodfacts.org/produit/5413121362639/chocolat-lait-caramel-sale-fair-trade',
        )

        self.product = Product.objects.get(name_product='Chocalat caramel')

        product = get_object_or_404(Product, pk=self.product.id)
        user = self.user.id
        save_user = get_object_or_404(User, pk=user)

        self.save = UserSaveProduct.objects.create(
            user_id=save_user,
            product_id=product
        )

    def test_search(self):
        client = Client()
        response = client.post('/library/login/', {'username': 'Test', 'password': 'testdjango'})
        self.assertEqual(response.status_code, 200)
        response = client.get('/library/saved/')
        self.assertContains(response, 'Chocalat caramel')


