# Generated by Django 2.0.7 on 2018-09-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimentacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimento',
            name='unidad',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]