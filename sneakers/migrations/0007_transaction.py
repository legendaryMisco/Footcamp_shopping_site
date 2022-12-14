# Generated by Django 4.0 on 2022-08-09 00:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_register_bio'),
        ('sneakers', '0006_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('fullname', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=300)),
                ('state', models.CharField(max_length=30)),
                ('zip_code', models.IntegerField()),
                ('transaction_items', models.TextField()),
                ('customer_id', models.UUIDField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.register')),
            ],
        ),
    ]
