from django.db import models


class ProductCategorie(models.Model):
    name_category = models.CharField(max_length=200)
    link_category = models.URLField()

    def __str__(self):
        return self.name_category


class Product(models.Model):

    name_product = models.CharField(max_length=250)
    categorie = models.ForeignKey(ProductCategorie, on_delete=models.CASCADE)
    nutriscore_product = models.CharField(max_length=1, blank=False)
    fat_100g = models.CharField(max_length=10, blank=True)
    sugars_100g = models.CharField(max_length=10, blank=True)
    saturated_fat_100g = models.CharField(max_length=10, blank=True)
    salt_100g = models.CharField(max_length=20, blank=True)
    image_product = models.URLField(blank=True)
    link_product = models.URLField(blank=True)

    def __str__(self):
        return self.name_product


class UserSaveProduct(models.Model):
    id_user = models.IntegerField(null=True)
    id_product = models.IntegerField(null=True)
    save_product = models.ForeignKey(ProductCategorie, on_delete=models.CASCADE)
