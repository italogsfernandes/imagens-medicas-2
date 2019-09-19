from django.contrib import admin

from .models import ImageModel

from django.utils.translation import ugettext as _


class ImageModelAdmin(admin.ModelAdmin):
    model = ImageModel
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    list_display = ['name', 'created_date', 'modified_date']
    fieldsets = [
        (_('Info'), {'fields': (
            'original_image',
            ('name', 'slug'),
            'user',
        )}),
    ]
    readonly_fields = ['created_date', 'modified_date']

admin.site.register(ImageModel, ImageModelAdmin)
