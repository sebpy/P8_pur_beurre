# Generated by Django 2.2.4 on 2019-09-04 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20190904_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='id_categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.ProductCategories'),
        ),
    ]
