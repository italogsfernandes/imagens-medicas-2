from django.views.generic import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'im2webapp/home.html',
            {'title': 'Imagens Médicas 2'}
        )


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'im2webapp/about.html', {'title': 'About'})
