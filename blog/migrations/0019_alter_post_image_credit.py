# Generated by Django 3.2.5 on 2021-08-01 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_tag_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_credit',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
