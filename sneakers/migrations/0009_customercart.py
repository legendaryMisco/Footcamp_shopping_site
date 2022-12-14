# Generated by Django 4.0 on 2022-08-12 18:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_register_bio'),
        ('sneakers', '0008_cart_transaction_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('customer_id', models.UUIDField(blank=True, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(default='unpaid', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product_name', models.ManyToManyField(to='sneakers.Cart')),
                ('transaction_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sneakers.transaction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.register')),
            ],
        ),
    ]
