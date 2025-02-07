# Generated by Django 5.1.6 on 2025-02-07 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('wallet_address', models.CharField(max_length=42)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=18)),
                ('ip_address', models.GenericIPAddressField()),
                ('status', models.CharField(choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')], max_length=20)),
            ],
        ),
    ]
