# Generated by Django 2.1.7 on 2019-05-10 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20190507_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
    ]
