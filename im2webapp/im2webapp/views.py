from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>IM2 Web App Home</h1>')


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>IM2 Web App About</h1>')
