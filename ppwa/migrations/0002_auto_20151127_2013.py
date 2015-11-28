# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppwa', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together=set([('name', 'phone', 'email')]),
        ),
    ]
