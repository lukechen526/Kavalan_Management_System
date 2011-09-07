#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import template
from django.utils.translation import ugettext

register = template.Library()

@register.inclusion_tag('kavalan_tags/bootstrap_fields.html')
def bootstrap_fields(form):
    return {'bootstrap_form': form}
