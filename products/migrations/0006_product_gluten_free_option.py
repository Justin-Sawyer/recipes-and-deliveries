# Generated by Django 3.2.4 on 2021-06-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_has_gluten'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gluten_free_option',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
