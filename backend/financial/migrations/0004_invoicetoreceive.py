# Generated by Django 5.0 on 2024-01-07 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0003_pixcharge'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceToReceive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField()),
                ('value', models.FloatField()),
                ('quantityParcel', models.PositiveIntegerField()),
                ('bankAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financial.bankaccount')),
            ],
        ),
    ]
