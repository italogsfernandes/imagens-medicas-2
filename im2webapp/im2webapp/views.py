from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from im2webapp.models import MedicalImage

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


class ImageEditorView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'im2webapp/image-editor.html',
            {'title': 'Imagens Médicas 2'}
        )


class ImageListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'im2webapp/image-list.html'
    model = MedicalImage

    def get(self, request, *args, **kwargs):
        if self.get_queryset().count() == 1:
            return redirect(self.get_queryset().first())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ImageListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
