from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import FormView
from django.shortcuts import render
from django import forms
import numpy as np
from decimal import Decimal as D

from .models import ImageModel


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'im2webapp/home.html',
            {'title': 'Home'}
        )


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'im2webapp/about.html', {'title': 'About'})


class ImageListView(LoginRequiredMixin, ListView):
    template_name = 'im2webapp/images_list.html'
    model = ImageModel
    ordering = "-modified_date"

    def get_queryset(self):
        user = self.request.user
        query = super().get_queryset()
        query = query.filter(user=user)
        return query


class ImageEditorView(LoginRequiredMixin, DetailView):
    template_name = 'im2webapp/image-editor.html'
    model = ImageModel
    query_pk_and_slug = True
    slug_url_kwarg = 'image_slug'
    context_object_name = 'image_object'


class ImageEditorLiteView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'im2webapp/image-editor-lite.html',
            {'title': 'Imagens Médicas 2'}
        )


# BH
class QuaternionForm(forms.Form):
    quaternion_w = forms.DecimalField(
        label='W',
        initial="1.00",
        min_value=D(-1.0),
        max_value=D(1.0),
        decimal_places=2,
    )
    quaternion_x = forms.DecimalField(
        label='X',
        initial="0.00",
        min_value=D(-1.0),
        max_value=D(1.0),
        decimal_places=2,
    )
    quaternion_y = forms.DecimalField(
        label='Y',
        initial="0.00",
        min_value=D(-1.0),
        max_value=D(1.0),
        decimal_places=2,
    )
    quaternion_z = forms.DecimalField(
        label='Z',
        initial="0.00",
        min_value=D(-1.0),
        max_value=D(1.0),
        decimal_places=2,
    )


class BeloHorizonteView(FormView):
    template_name = 'im2webapp/belo-horizonte.html'
    form_class = QuaternionForm
    quaternion = np.array([1, 0, 0, 0], dtype=float)
    success_url = 'belo-horizonte'
