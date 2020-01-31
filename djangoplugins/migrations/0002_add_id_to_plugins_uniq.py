# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dirtyfields.dirtyfields


class Migration(migrations.Migration):

    dependencies = [
        ('djangoplugins', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='plugin',
            unique_together=set([('point', 'name', 'index')]),
        ),
    ]
