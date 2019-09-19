from django.urls import path
from django.conf.urls import url

from .views import (
    HomeView,
    AboutView,
    ImageEditorView,
    ImageEditorLiteView,
    BeloHorizonteView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('image-editor/', ImageEditorLiteView.as_view(), name='image-editor'),
    url(
        r'^image-editor/(?P<image_slug>[-0-9A-Za-z]+)/$',
        ImageEditorView.as_view(),
        name='image-editor'
    ),
    path('belo-horizonte', BeloHorizonteView.as_view(), name='belo-horizonte'),
]
