# Generated by Django 3.0.8 on 2020-07-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='bidder',
            field=models.CharField(blank='true', max_length=512),
        ),
    ]
