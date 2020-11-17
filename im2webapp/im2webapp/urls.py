from django.urls import path
from django.conf.urls import url

from .views import (
    HomeView,
    AboutView,
    ImageListView,
    ImageEditorView,
    ImageEditorLiteView,
    UploadImageView,
    UploadImageGroupView,
    ImageAddIntensityModifierView,
    ImageAddNoiseModifierView,
    ImageAddFilterModifierView,
    ResetImageRedirectView,
    UndoModifierRedirectView,
    EqualizeImageModifierView,
    ImageGroupListView,
    ProcessarView,
    ClassificarView,
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
    path(
        'groups/<group_slug>/',
        ImageGroupListView.as_view(),
        name='image-group-details'
    ),
    path(
        'groups/<group_slug>/processar/',
        ProcessarView.as_view(),
        name='image-group-processar'
    ),
    path(
        'groups/<group_slug>/classificar/',
        ClassificarView.as_view(),
        name='image-group-classificar'
    ),
    url('images/', ImageListView.as_view(), name='images_list'),
    path('upload-image/', UploadImageView.as_view(), name='view_upload_image'),
    path('upload-image-group/', UploadImageGroupView.as_view(),
         name='view_upload_image_group'),
    url(
        'add_intensity_modifier/',
        ImageAddIntensityModifierView.as_view(),
        name='add_intensity_modifier'
    ),
    url(
        'add_noise_modifier/',
        ImageAddNoiseModifierView.as_view(),
        name='add_noise_modifier'
    ),
    url(
        'add_filter_modifier/',
        ImageAddFilterModifierView.as_view(),
        name='add_filter_modifier'
    ),
    path(
        'reset_image/<image_slug>/',
        ResetImageRedirectView.as_view(),
        name='reset_image_url'
    ),
    path(
        'undo_modifier/<image_slug>/',
        UndoModifierRedirectView.as_view(),
        name='undo_modifier_url'
    ),
    path(
        'equalize_img/<image_slug>/',
        EqualizeImageModifierView.as_view(),
        name='url_equalize'
    )
]
