# Generated by Django 4.0 on 2022-08-08 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0004_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='product_id',
            field=models.UUIDField(default=None),
            preserve_default=False,
        ),
    ]
