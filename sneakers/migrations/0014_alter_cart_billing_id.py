# Generated by Django 4.0 on 2022-09-03 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0013_cart_billing_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='billing_id',
            field=models.UUIDField(default=None, editable=False),
            preserve_default=False,
        ),
    ]
