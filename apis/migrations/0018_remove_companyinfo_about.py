# Generated by Django 4.0.7 on 2022-09-09 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0017_companyinfo_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyinfo',
            name='about',
        ),
    ]
