# Generated by Django 2.1.1 on 2019-11-03 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cosmetic', '0009_product_image_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Interested_Cosmetic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cosmetic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cosmetic.Cosmetic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]