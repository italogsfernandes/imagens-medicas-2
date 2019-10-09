from django.urls import path
from django.conf.urls import url

from .views import (
    HomeView,
    AboutView,
    ImageListView,
    ImageEditorView,
    ImageEditorLiteView,
    BeloHorizonteView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('lite-editor/', ImageEditorLiteView.as_view(), name='lite-editor'),
    path(
        'image-editor/<image_slug>/',
        ImageEditorView.as_view(),
        name='image-editor'
    ),
    url('images/', ImageListView.as_view(), name='images_list'),
    path('belo-horizonte', BeloHorizonteView.as_view(), name='belo-horizonte'),
]
