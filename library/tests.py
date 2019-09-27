from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User

from library.models import ProductCategorie, Product, UserSaveProduct
from library.views import profile, search, save_product
from library.forms import LoginForm, RegisterForm


class IndexPageTestCase(TestCase):
    """ Test index page """
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    """ Test index page """
    def test_legal_page(self):
        response = self.client.get(reverse('legal_notice'))
        self.assertEqual(response.status_code, 200)


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
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test@django.fr')


class TestLoginFormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user(username="Test",
                                 email="test@django.fr",
                                 password="testdjango")

        self.user = User.objects.get(username='Test')

    def test_valid_form(self):
        username = self.user.username
        password = self.user.password
        data = {'username': username, 'password': password, }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'username': '', 'password': '', }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


class TestRegisterFormTestCase(TestCase):

    def test_valid_form(self):
        user_register = User.objects.create_user(username="Test",
                                                 email="test@django.fr",
                                                 password="testdjango")
        data = {'username': user_register.username, 'email': user_register.email, 'password1': user_register.password,
                'password2': user_register.password, }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user_register = User.objects.create_user(username="Test",
                                                 email="test@django.fr",
                                                 password="")
        data = {'username': user_register.username, 'email': user_register.email, 'password': user_register.password, }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())


class TestSaveTestCase(TestCase):
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


class TestSearchTestCase(TestCase):
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
