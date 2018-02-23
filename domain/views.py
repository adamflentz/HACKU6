# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.gis.geoip2 import GeoIP2
from .forms import DomainForm
# Create your views here.

# Create your views here.
class home(TemplateView):
    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        form = DomainForm()
        try:
            if x_forwarded_for:
                print ("returning FORWARDED_FOR")
                ip = x_forwarded_for.split(',')[-1].strip()
            elif request.META.get('HTTP_X_REAL_IP'):
                print ("returning REAL_IP")
                ip = request.META.get('HTTP_X_REAL_IP')
            else:
                print ("returning REMOTE_ADDR")
                ip = request.META.get('REMOTE_ADDR')
        except:
            x_forwarded_for = '128.101.101.101'

        ip = '128.101.101.101'

        print(ip)
        Geo = GeoIP2()
        currcity = Geo.city(ip)
        print(currcity)
        lat = currcity.get('latitude')
        lng = currcity.get('longitude')
        return render(request, 'home.html', locals())

class results(TemplateView):
    def get(self, request):
        query = request.GET.get("search")
        domain = request.GET.get("domain")
        print(query)
        print(domain)
        return render(request, "results.html",locals())

    def post(self, request):
        search = request.POST.get('search')
        print(search)
        return render(request, "results.html", locals())