# Generated by Django 2.1.1 on 2019-11-01 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetic', '0007_auto_20191101_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag_names',
            field=models.ManyToManyField(to='cosmetic.Tag'),
        ),
    ]
