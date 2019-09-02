from django.db import models


class ProductCategories(models.Model):
    name_category = models.CharField(max_length=200)
    link_category = models.URLField()


class Products(models.Model):
    name_product = models.CharField(max_length=250)
    brand_product = models.CharField(max_length=250)
    id_categories = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    description_product = models.CharField(max_length=200)
    nutriscore_product = models.CharField(max_length=1)
    store_product = models.CharField(max_length=200)
    link_product = models.URLField()


class Users(models.Model):
    login = models.CharField(max_length=50)
    mail = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)


class UserSaveProduct(models.Model):
    id_user = models.IntegerField(null=True)
    id_product = models.IntegerField(null=True)
    save_product = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
