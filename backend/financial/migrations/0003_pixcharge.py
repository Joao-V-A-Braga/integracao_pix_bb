# Generated by Django 5.0 on 2024-01-03 01:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0002_pixaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='PixCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField()),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)])),
                ('status', models.SmallIntegerField(default=1)),
                ('expiration', models.PositiveIntegerField()),
                ('code', models.CharField()),
                ('txid', models.CharField()),
                ('location', models.CharField()),
                ('e2eid', models.CharField(blank=True, null=True)),
                ('pixAccount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financial.pixaccount')),
            ],
        ),
    ]
