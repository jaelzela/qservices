# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=200)
    service_description = models.TextField()
    category = models.CharField(default='', max_length=200)
    reputation = models.FloatField(default=0.0)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    service_id = models.IntegerField()
    review_text = models.TextField()
    review_date = models.CharField(max_length=20)
    review_polarity = models.CharField(max_length=3)


class Rate(models.Model):
    rate_id = models.AutoField(primary_key=True)
    review_id = models.IntegerField()
    rate_polarity = models.CharField(max_length=3)
