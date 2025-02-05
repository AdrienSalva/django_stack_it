# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [path("admin/", admin.site.urls)] + i18n_patterns(
    path("", include("stack_it.urls"))
)
