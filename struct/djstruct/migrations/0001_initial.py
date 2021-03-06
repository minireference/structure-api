# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-05-20 08:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('kind', models.CharField(max_length=1000)),
                ('path', models.CharField(max_length=1000)),
                ('scope', models.CharField(default='miniref', max_length=1000)),
                ('version', models.CharField(default='0.1', max_length=1000, verbose_name='schema version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('level', models.CharField(default='All', max_length=1000, verbose_name='Educational level')),
            ],
        ),
        migrations.CreateModel(
            name='ContainmentRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explain_contains', models.CharField(max_length=1000, null=True, verbose_name='Explain contains')),
                ('explain_ispartof', models.CharField(max_length=1000, null=True, verbose_name='Explain is-part-of relation')),
                ('level', models.CharField(default='All', max_length=1000, verbose_name='Educational level')),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parent_rels', to='djstruct.BaseNode')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_rels', to='djstruct.BaseNode')),
            ],
        ),
        migrations.CreateModel(
            name='DependencyRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explain_prerequisite', models.CharField(max_length=1000, null=True, verbose_name='Explain why prerequsite is needed')),
                ('explain_usedfor', models.CharField(max_length=1000, null=True, verbose_name='Explain the application')),
                ('level', models.CharField(default='All', max_length=1000, verbose_name='Educational level')),
                ('prerequisite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prerequisites_rels', to='djstruct.BaseNode')),
                ('usedfor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usedfors_rels', to='djstruct.BaseNode')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explain_related', models.CharField(max_length=1000, null=True, verbose_name='Explain related')),
                ('level', models.CharField(default='All', max_length=1000, verbose_name='Educational level')),
                ('left', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='right_rels', to='djstruct.BaseNode')),
                ('right', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='left_rels', to='djstruct.BaseNode')),
            ],
        ),
        migrations.AddField(
            model_name='basenode',
            name='contents',
            field=models.ManyToManyField(related_name='parents', through='djstruct.ContainmentRelation', to='djstruct.BaseNode'),
        ),
        migrations.AddField(
            model_name='basenode',
            name='prerequsites',
            field=models.ManyToManyField(related_name='usedfors', through='djstruct.DependencyRelation', to='djstruct.BaseNode'),
        ),
        migrations.AddField(
            model_name='basenode',
            name='related',
            field=models.ManyToManyField(related_name='_basenode_related_+', through='djstruct.RelatedRelation', to='djstruct.BaseNode'),
        ),
        migrations.AlterUniqueTogether(
            name='basenode',
            unique_together=set([('scope', 'path')]),
        ),
    ]
