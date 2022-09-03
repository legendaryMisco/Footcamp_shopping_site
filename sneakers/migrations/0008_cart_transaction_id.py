# Generated by Django 4.0 on 2022-08-09 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0007_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='transaction_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sneakers.transaction'),
        ),
    ]
