# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from serv.models import Category, Service, Review, Rate


def index(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) > 0:
            services = Service.objects.filter(service_name__contains=query)
            return render(request, "services.html", dict(services=services))
        else:
            return render(request, "index.html", dict())
    raise Http404
