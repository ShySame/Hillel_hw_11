# Generated by Django 3.2.6 on 2021-09-21 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='about',
            field=models.TextField(max_length=100),
            preserve_default=False,
        ),
    ]