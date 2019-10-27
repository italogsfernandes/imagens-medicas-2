from django.forms import HiddenInput, NumberInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    DetailView,
    ListView,
    CreateView
)
from django.urls import reverse_lazy
from django.shortcuts import render

from im2webapp.models import (
    ImageModel,
    ItensityImageModifier,
)

from im2webapp.forms import (
    ImageModelForm,
    AddIntensityModifierForm,
    AddNoiseModifierForm,
)


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

    def get_context_data(self, **kwargs):
        context = super(ImageEditorView, self).get_context_data(**kwargs)
        # Brightness
        brightness_form = AddIntensityModifierForm(
            initial=dict(
                type_of_modifier=ItensityImageModifier.BRIGHTNESS,
                argument_name=_("shades"),
                argument_value=0,
                imagem=context['image_object'].pk,
            )
        )
        brightness_form.fields['argument_value'].label = _('Brightness: ')
        brightness_form.fields['argument_value'].widget = NumberInput(
         attrs={'type': 'range', 'min': '-255', 'step': '1', 'max': '255'},
        )
        # Intensity
        intensity_form = AddIntensityModifierForm(
            initial=dict(
                imagem=context['image_object'].pk,
            )
        )
        # Noise
        noise_form = AddNoiseModifierForm(
            initial=dict(
                imagem=context['image_object'].pk,
            )
        )
        # Context
        context['brightness_form'] = brightness_form
        context['intensity_form'] = intensity_form
        context['noise_form'] = noise_form
        return context


class ImageEditorLiteView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'im2webapp/image-editor-lite.html',
            {'title': 'Imagens Médicas 2'}
        )


class UploadImageView(CreateView):
    model = ImageModel
    form_class = ImageModelForm
    template_name = 'im2webapp/upload_image_view.html'
    success_url = reverse_lazy('images_list')

    def get_context_data(self, **kwargs):
        context = super(UploadImageView, self).get_context_data(**kwargs)
        # This sets the initial value for the field:
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        return context
