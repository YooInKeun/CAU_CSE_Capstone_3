# Generated by Django 2.1.1 on 2019-10-28 17:48

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cosmetic',
            name='test',
        ),
        migrations.AddField(
            model_name='cosmetic',
            name='brand_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='cosmetic',
            name='cosmetic_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='cosmetic',
            name='image_link',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='cosmetic',
            name='option_names',
            field=jsonfield.fields.JSONField(default=''),
        ),
        migrations.AddField(
            model_name='cosmetic',
            name='tag_names',
            field=jsonfield.fields.JSONField(default=''),
        ),
    ]
