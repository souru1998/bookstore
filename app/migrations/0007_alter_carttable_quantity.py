# Generated by Django 4.2.2 on 2023-08-09 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_carttable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carttable',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
