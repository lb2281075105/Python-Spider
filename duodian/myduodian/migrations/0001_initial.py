# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AiDuoDian',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.CharField(max_length=1000)),
                ('goodName', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=40)),
            ],
        ),
    ]
