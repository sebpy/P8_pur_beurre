from django.db import models


class ProductCategories(models.Model):
    name_category = models.CharField(max_length=200)
    link_category = models.URLField()

    def __str__(self):
        return self.name_category


class Products(models.Model):
    NUTRI_GRADE = (
        (0, "N/A"),
        (1, "A"),
        (2, "B"),
        (3, "C"),
        (4, "D"),
        (5, "E"),
    )

    name_product = models.CharField(max_length=250)
    brand_product = models.CharField(max_length=250)
    #id_categories = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    id_categories = models.CharField(max_length=11)
    description_product = models.CharField(max_length=200, blank=True)
    nutriscore_product = models.SmallIntegerField(choices=NUTRI_GRADE, default=0, blank=True)
    image_product = models.URLField(blank=True)
    link_product = models.URLField(blank=True)

    def __str__(self):
        return self.name_product


class Users(models.Model):
    login = models.CharField(max_length=50)
    mail = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)


class UserSaveProduct(models.Model):
    id_user = models.IntegerField(null=True)
    id_product = models.IntegerField(null=True)
    save_product = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
