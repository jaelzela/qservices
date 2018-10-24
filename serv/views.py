# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


def index(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) > 0:
            json_url = os.path.join(SITE_ROOT, 'static/json', 'exchange.json')
            json_data = open(json_url)
            data = json.load(json_data)
        else:
            return render(request, "index.html", dict())
    raise Http404
