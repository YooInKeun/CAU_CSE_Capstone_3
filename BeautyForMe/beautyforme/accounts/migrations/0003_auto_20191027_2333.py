# Generated by Django 2.1.1 on 2019-10-27 14:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191013_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
        migrations.AddField(
            model_name='profile',
            name='address_detail',
            field=models.TextField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='profile',
            name='zip_code',
            field=models.TextField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.TextField(max_length=10, null=True),
        ),
    ]
