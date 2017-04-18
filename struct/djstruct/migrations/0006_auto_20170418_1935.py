# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-18 19:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djstruct', '0005_auto_20160617_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='djangobasenode',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='djangobasenode',
            name='path',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='djangobasenode',
            name='scope',
            field=models.CharField(default='miniref', max_length=1000),
        ),
        migrations.AlterField(
            model_name='djangodependencyrelation',
            name='explain_prerequisite',
            field=models.CharField(max_length=1000, null=True, verbose_name='Explain why prerequsite is needed'),
        ),
        migrations.AlterField(
            model_name='djangodependencyrelation',
            name='explain_usedfor',
            field=models.CharField(max_length=1000, null=True, verbose_name='Explain the application'),
        ),
        migrations.AlterField(
            model_name='djangodependencyrelation',
            name='prerequisite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prerequisites_rels', to='djstruct.DjangoBaseNode'),
        ),
        migrations.AlterField(
            model_name='djangodependencyrelation',
            name='usedfor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usedfors_rels', to='djstruct.DjangoBaseNode'),
        ),
        migrations.AlterUniqueTogether(
            name='djangobasenode',
            unique_together=set([('scope', 'path')]),
        ),
    ]
