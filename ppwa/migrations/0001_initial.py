# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(help_text=b'Price at time of purchase.', max_digits=10, decimal_places=2)),
                ('quantity', models.PositiveIntegerField(help_text=b'Quantity Ordered.')),
                ('confirmation', models.CharField(help_text=b'Confirmation code from purchase API.', max_length=255)),
                ('customer', models.ForeignKey(to='ppwa.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=60)),
                ('uuid', models.UUIDField(db_index=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'Set false if product no longer "carried".')),
                ('date_updated', models.DateTimeField(help_text=b'Set by data updater.')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='ppwa.Product'),
        ),
    ]
