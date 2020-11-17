from django.template.loader import render_to_string
from django.forms import HiddenInput, NumberInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    RedirectView
)
from django.http import JsonResponse
from django.contrib import messages
from im2webapp.utils import redirect_to_referrer, safe_referrer
from django.utils.http import is_safe_url
from django.shortcuts import get_object_or_404

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
    ImageGroupModel,
    IntensityImageModifier,
)

from im2webapp.forms import (
    ImageModelForm,
    ImageGroupModelForm,
    AddIntensityModifierForm,
    AddNoiseModifierForm,
    AddFilterModifierForm,
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

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        objects_list = context['object_list']
        context['image_standalone'] = objects_list.filter(image_group__isnull=True)
        context['image_in_groups'] = objects_list.filter(image_group__isnull=False).order_by('image_group', 'name')
        return context


class ImageGroupListView(LoginRequiredMixin, DetailView):
    template_name = 'im2webapp/image_group_details.html'
    model = ImageGroupModel
    query_pk_and_slug = True
    slug_url_kwarg = 'group_slug'
    context_object_name = 'group_object'

    def get_context_data(self, **kwargs):
        context = super(ImageGroupListView, self).get_context_data(**kwargs)
        context['object_list'] = self.object.imagemodel_set.all().order_by("name")
        return context


class ResetImageRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.image_model = get_object_or_404(
            ImageModel, slug=kwargs['image_slug'], user=request.user
        )
        self.image_model.intensityimagemodifier_set.all().delete()
        self.image_model.noiseimagemodifier_set.all().delete()
        self.image_model.filterimagemodifier_set.all().delete()
        self.image_model.reset_edited_image()
        if request.is_ajax():
            return self.get_ajax(request, *args, **kwargs)
        return redirect_to_referrer(request, 'images_list')

    def get_ajax(self, request, *args, **kwargs):
        image_object = self.image_model

        actions_history = (
            image_object.get_modifiers_list()
        )
        context = {
            'actions_history': actions_history,
            'image_object': image_object,
        }
        tab_info_content = render_to_string(
            'im2webapp/blocks/_tab_info_content.html',
            context=context,
            request=request,
        )
        history_content = render_to_string(
            'im2webapp/_block_image_history.html',
            context=context,
            request=request,
        )
        m = render_to_string('im2webapp/_messages.html', request=request)
        return JsonResponse({
            'tab_info_content': tab_info_content,
            'history_content_div': history_content,
            'messages': m,
            'edited_image_url': image_object.edited_image.url,
        })


class EqualizeImageModifierView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.image_model = get_object_or_404(
            ImageModel, slug=kwargs['image_slug'], user=request.user
        )
        self.image_model.do_equalize()
        messages.success(request, "Imagem Equalizada!")
        return redirect_to_referrer(request, 'images_list')


class ProcessarView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.image_group = get_object_or_404(
            ImageGroupModel, slug=kwargs['group_slug'], user=request.user
        )
        msg = self.image_group.processar()
        messages.success(request, msg)
        return redirect_to_referrer(request, 'images_list')


class ClassificarView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.image_group = get_object_or_404(
            ImageGroupModel, slug=kwargs['group_slug'], user=request.user
        )
        msg = self.image_group.classificar()
        messages.success(request, msg)
        return redirect_to_referrer(request, 'images_list')


class UndoModifierRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.image_model = get_object_or_404(
            ImageModel, slug=kwargs['image_slug'], user=request.user
        )
        modifier_to_be_undone = self.image_model.get_modifiers_list().first()
        if modifier_to_be_undone['modifier'] == 'intensity':
            obj_to_delete = self.image_model.intensityimagemodifier_set.get(
                pk=modifier_to_be_undone['pk']
            )
            obj_to_delete.delete()
        elif modifier_to_be_undone['modifier'] == 'noise':
            obj_to_delete = self.image_model.noiseimagemodifier_set.get(
                pk=modifier_to_be_undone['pk']
            )
            obj_to_delete.delete()
        elif modifier_to_be_undone['modifier'] == 'filter':
            obj_to_delete = self.image_model.filterimagemodifier_set.get(
                pk=modifier_to_be_undone['pk']
            )
            obj_to_delete.delete()

        self.image_model.reset_edited_image()
        self.image_model.apply_all_modifiers()
        if request.is_ajax():
            return self.get_ajax(request, *args, **kwargs)
        return redirect_to_referrer(request, 'images_list')

    def get_ajax(self, request, *args, **kwargs):
        image_object = self.image_model

        actions_history = (
            image_object.get_modifiers_list()
        )
        context = {
            'actions_history': actions_history,
            'image_object': image_object,
        }
        tab_info_content = render_to_string(
            'im2webapp/blocks/_tab_info_content.html',
            context=context,
            request=request,
        )
        history_content = render_to_string(
            'im2webapp/_block_image_history.html',
            context=context,
            request=request,
        )
        m = render_to_string('im2webapp/_messages.html', request=request)
        return JsonResponse({
            'tab_info_content': tab_info_content,
            'history_content_div': history_content,
            'messages': m,
            'edited_image_url': image_object.edited_image.url,
        })


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
                type_of_modifier=IntensityImageModifier.BRIGHTNESS,
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
        # Filters
        filters_form = AddFilterModifierForm(
            initial=dict(
                imagem=context['image_object'].pk,
            )
        )
        # actions_history
        actions_history = (
            context['image_object'].get_modifiers_list()
        )
        # Edited image
        edited_image = (
            context['image_object'].edited_image
        )
        if not edited_image:
            context['image_object'].reset_edited_image()
            edited_image = (
                context['image_object'].edited_image
            )

        # Context
        context['brightness_form'] = brightness_form
        context['intensity_form'] = intensity_form
        context['noise_form'] = noise_form
        context['filters_form'] = filters_form
        context['actions_history'] = actions_history
        context['edited_image'] = edited_image
        return context

    def get_queryset(self):
        self.queryset = ImageModel.objects.filter(
            user=self.request.user
        )
        return super().get_queryset()


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


class UploadImageGroupView(CreateView):
    model = ImageGroupModel
    form_class = ImageGroupModelForm
    template_name = 'im2webapp/upload_image_group_view.html'
    success_url = reverse_lazy('images_list')

    def get_context_data(self, **kwargs):
        context = super(UploadImageGroupView, self).get_context_data(**kwargs)
        # This sets the initial value for the field:
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        return context


class ImageAddIntensityModifierView(CreateView):
    form_class = AddIntensityModifierForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post_return_value = super(ImageAddIntensityModifierView, self).post(
            request, *args, **kwargs
        )
        self.object.apply_modifier()

        if request.is_ajax():
            return self.post_ajax(request, *args, **kwargs)

        return post_return_value

    def post_ajax(self, request, *args, **kwargs):
        image_object = self.object.imagem

        actions_history = (
            image_object.get_modifiers_list()
        )
        context = {
            'actions_history': actions_history,
            'image_object': image_object,
        }
        history_content = render_to_string(
            'im2webapp/_block_image_history.html',
            context=context,
            request=request,
        )
        m = render_to_string('im2webapp/_messages.html', request=request)
        return JsonResponse({
         'history_content_div': history_content,
         'messages': m,
         'edited_image_url': image_object.edited_image.url,
        })

    def form_invalid(self, form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))

        return redirect_to_referrer(self.request, 'images_list')

    def get_success_url(self):
        post_url = self.request.POST.get('next')
        host = self.request.get_host()
        if post_url and is_safe_url(url=post_url, allowed_hosts=[host]):
            return post_url
        return safe_referrer(self.request, 'images_list')


class ImageAddNoiseModifierView(CreateView):
    form_class = AddNoiseModifierForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post_return_value = super(ImageAddNoiseModifierView, self).post(
            request, *args, **kwargs
        )
        self.object.apply_modifier()

        if request.is_ajax():
            return self.post_ajax(request, *args, **kwargs)

        return post_return_value

    def post_ajax(self, request, *args, **kwargs):
        image_object = self.object.imagem

        actions_history = (
            image_object.get_modifiers_list()
        )
        context = {
            'actions_history': actions_history,
            'image_object': image_object,
        }
        history_content = render_to_string(
            'im2webapp/_block_image_history.html',
            context=context,
            request=request,
        )
        m = render_to_string('im2webapp/_messages.html', request=request)
        return JsonResponse({
         'history_content_div': history_content,
         'messages': m,
         'edited_image_url': image_object.edited_image.url,
        })

    def form_invalid(self, form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))

        return redirect_to_referrer(self.request, 'images_list')

    def get_success_url(self):
        post_url = self.request.POST.get('next')
        host = self.request.get_host()
        if post_url and is_safe_url(url=post_url, allowed_hosts=[host]):
            return post_url
        return safe_referrer(self.request, 'images_list')


class ImageAddFilterModifierView(CreateView):
    form_class = AddFilterModifierForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        post_return_value = super(ImageAddFilterModifierView, self).post(
            request, *args, **kwargs
        )
        self.object.apply_modifier()

        if request.is_ajax():
            return self.post_ajax(request, *args, **kwargs)

        return post_return_value

    def post_ajax(self, request, *args, **kwargs):
        image_object = self.object.imagem

        actions_history = (
            image_object.get_modifiers_list()
        )
        context = {
            'actions_history': actions_history,
            'image_object': image_object,
        }
        history_content = render_to_string(
            'im2webapp/_block_image_history.html',
            context=context,
            request=request,
        )
        m = render_to_string('im2webapp/_messages.html', request=request)
        return JsonResponse({
         'history_content_div': history_content,
         'messages': m,
         'edited_image_url': image_object.edited_image.url,
        })

    def form_invalid(self, form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))

        return redirect_to_referrer(self.request, 'images_list')

    def get_success_url(self):
        post_url = self.request.POST.get('next')
        host = self.request.get_host()
        if post_url and is_safe_url(url=post_url, allowed_hosts=[host]):
            return post_url
        return safe_referrer(self.request, 'images_list')
