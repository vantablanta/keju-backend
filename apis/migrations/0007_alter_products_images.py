# Generated by Django 4.0.7 on 2022-09-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_alter_products_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='images',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
