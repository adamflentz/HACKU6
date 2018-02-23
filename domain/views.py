# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.gis.geoip2 import GeoIP2
from .forms import DomainForm
import requests, json
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
                if ip == '127.0.0.1':
                    x_forwarded_for = '128.101.101.101'
                    ip = x_forwarded_for
        except:
            x_forwarded_for = '128.101.101.101'


        print(ip)
        Geo = GeoIP2()
        currcity = Geo.city(ip)
        print(currcity)
        lat = currcity.get('latitude')
        lng = currcity.get('longitude')
        resp = requests.get('http://api.geonames.org/findNearbyPostalCodesJSON?lat=' + str(lat) + '&lng=' + str(
            lng) + '&radius=30&username=tnraddatz')
        if resp.status_code != 200:
            # This means something went wrong.
            print("ERROR:   ")
            raise TimeoutError('GET /tasks/ {}'.format(resp.status_code))

        # This tries to remove the pre-fix data "postalCodes" from JSON
        # The goal is to convert the response into pure json
        resp = resp.text
        index = 0
        print("hello")
        for letter in resp:
            if letter == "[":
                resp = resp[index + 1:-2]
                break
            index += 1
        resp = '[' + resp + ']'

        resp = json.loads(resp)  # dictionary

        respList = []
        for name in resp:
            i = 0
            respList.append(name['placeName']) #can modify or add more keys if necessary
        respList = set(respList)
        respList = list(respList)
        print(respList)
        return render(request, 'home.html', {"locations": respList, "form": form, "lat": lat, "lng": lng})

class results(TemplateView):
    def get(self, request):




        return render(request, "results.html",locals())

    def post(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            extension = form.cleaned_data['extension']
            if extension == None:
                extension = ".autos"
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
                    if ip == '127.0.0.1':
                        x_forwarded_for = '128.101.101.101'
                        ip = x_forwarded_for
            except:
                x_forwarded_for = '128.101.101.101'

            print(ip)
            Geo = GeoIP2()
            currcity = Geo.city(ip)
            print(currcity)
            lat = currcity.get('latitude')
            lng = currcity.get('longitude')
            resp = requests.get('http://api.geonames.org/findNearbyPostalCodesJSON?lat=' + str(lat) + '&lng=' + str(
                lng) + '&radius=30&username=tnraddatz')
            if resp.status_code != 200:
                # This means something went wrong.
                print("ERROR:   ")
                raise TimeoutError('GET /tasks/ {}'.format(resp.status_code))

            # This tries to remove the pre-fix data "postalCodes" from JSON
            # The goal is to convert the response into pure json
            resp = resp.text
            index = 0
            print("hello")
            for letter in resp:
                if letter == "[":
                    resp = resp[index + 1:-2]
                    break
                index += 1
            resp = '[' + resp + ']'

            resp = json.loads(resp)  # dictionary

            respList = []
            domainOutput = []
            for name in resp:
                i = 0
                respList.append(name['placeName'].lower().replace(" ", "-"))  # can modify or add more keys if necessary
            respList = set(respList)
            respList = list(respList)
            print(respList)
            query = domain
            print(query)
            print("got data")
            itemlist = [query]
            terms = ['ml', 'rel_jjb','rel_rhy'] #api search tags
            for tag in terms:
                #call API and get the JSON file for our query
                searchurl = 'http://api.datamuse.com/words?' + tag + '=' + query
                print(searchurl)
                meansLikeResponse = requests.get(searchurl)
                #responseText = meansLikeResponse.text
                responseJson = meansLikeResponse.json()

                #take top 10 results from query and place in our final 'to search' list
                count = 0
                for item in responseJson:
                    if tag == 'ml' or tag == 'rel_rhy':
                        itemlist.append(item["word"].replace(" ", "-"))
                    elif tag == 'rel_jjb':
                        itemlist.append(item["word"] + "-" +query)
                    #add geo tags to our 'means like' queries
                    if count == 0 and tag == 'ml':
                        for element in respList:
                            itemlist.append(element+ "-" + item["word"])
                    if count == 9:
                        break
                    count += 1
            print(itemlist)
            header = "X-NAMESUGGESTION -APIKEY:676226de70489ae087ba1cd63cf9345a"
            for item in itemlist:
                urlresponse = requests.get('https://sugapi.verisign-grs.com/ns-api/2.0/suggest?name=' + item + '&tlds=' + extension)
                urljson = json.loads(urlresponse.text)
                print(urljson)
                if urljson == {}:
                    print("empty")
                domainlist = urljson["results"]
                domainOutput.append(domainlist[0])
            print(domainOutput)
            return render(request, "results.html", locals())

class about(TemplateView):
    def get(self, request):
        return render(request, "about.html", locals())

class contact(TemplateView):
    def get(self, request):
        return render(request,"contact.html",locals())