from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from .models import DjangoBaseNode


@admin.register(DjangoBaseNode)
class DjangoBaseNodeAdmin(admin.ModelAdmin):
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    list_display = ('id',
                   'scope',
                   'path',
                   'comment',
                   'created_at',
                   'modified_at',)
