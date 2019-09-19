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


class ImageListView(ListView):
    pass


class ImageEditorView(DetailView):
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

    def form_valid(self, form):
        self.quaternion[0] = float(form.cleaned_data['quaternion_w'])
        self.quaternion[1] = float(form.cleaned_data['quaternion_x'])
        self.quaternion[2] = float(form.cleaned_data['quaternion_y'])
        self.quaternion[3] = float(form.cleaned_data['quaternion_z'])
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Belo Horizonte"
        context['quaternion'] = self.quaternion
        return context

    def get_initial(self, *args, **kwargs):
        initial = {
            'quaternion_w': self.quaternion[0],
            'quaternion_x': self.quaternion[1],
            'quaternion_y': self.quaternion[2],
            'quaternion_z': self.quaternion[3],
        }
        return initial

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
