# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from serv.models import Service, Review, Rate


def index(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) > 0:
            services = Service.objects.filter(Q(service_name__contains=query) | Q(category__contains=query))
            services = sorted(services, key=lambda x: x.reputation, reverse=True)
            for service in services:
                service.logo = service.service_name.lower().replace(' ', '-').replace('.', '-')

            return render(request, "services.html", dict(services=services))
        else:
            return render(request, "index.html", dict())
    raise Http404


def reviews(request, service_id):
    if request.method == 'GET':
        service = Service.objects.get(service_id=service_id)
        service.logo = service.service_name.lower().replace(' ', '-').replace('.', '-')

        reviews = Review.objects.filter(service_id=service_id)
        return render(request, "service.html", dict(service=service, reviews=reviews))
    raise Http404
