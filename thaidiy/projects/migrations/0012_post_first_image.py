# Generated by Django 2.1.7 on 2019-05-12 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20190510_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='first_image',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
