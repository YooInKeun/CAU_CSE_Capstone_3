# Generated by Django 2.1.5 on 2019-11-28 15:30

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('thumbnail', models.TextField(default='')),
                ('link', models.TextField(default='')),
                ('upload_date', models.DateField(default='', max_length=100)),
                ('hits', models.IntegerField(default=0)),
                ('cosmetics', jsonfield.fields.JSONField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Youtuber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='youtuber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeup.Youtuber'),
        ),
    ]
