# Generated by Django 3.0.8 on 2020-07-16 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_item_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank='true', max_length=10000),
        ),
    ]
