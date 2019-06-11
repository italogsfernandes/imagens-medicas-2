from django.urls import path
from .views import (
    HomeView,
    AboutView,
    ImageEditorView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('image-editor', ImageEditorView.as_view(), name='image-editor'),
]
