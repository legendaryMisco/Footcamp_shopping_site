# Generated by Django 4.0 on 2022-09-03 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0015_alter_cart_billing_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='billing_id',
            new_name='billings_id',
        ),
    ]
