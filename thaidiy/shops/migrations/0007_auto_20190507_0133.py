# Generated by Django 2.1.7 on 2019-05-07 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_auto_20190502_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='details',
            field=models.TextField(max_length=10000),
        ),
    ]
