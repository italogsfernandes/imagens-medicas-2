from django.contrib import admin
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.utils.safestring import mark_safe

from im2webapp.models import MedicalImage


class MedicalImageAdmin(admin.ModelAdmin):
    model = MedicalImage
    prepopulated_fields = {"slug": ("name",)}
    list_display = [
        'name', 'user', 'created_date', 'modified_date', 'go_to_page'
    ]
    readonly_fields = ['go_to_page', ]

    def go_to_page(self, instance):
        href = reverse('image-list')
        if instance.pk and instance.slug:
            href = reverse('image-editor', args=[instance.slug])
        return mark_safe(
            '<a href="{url}">{text}</a>'.format(url=href, text=_('Go to page'))
        )

    go_to_page.allow_tags = True
    go_to_page.short_description = _('Link')


admin.site.register(MedicalImage, MedicalImageAdmin)
