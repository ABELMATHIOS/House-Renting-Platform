# Generated by Django 5.2 on 2025-05-02 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Listing', '0005_rename_listing_listingmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingmodel',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
