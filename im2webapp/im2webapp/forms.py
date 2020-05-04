from django import forms
from django.template.defaultfilters import slugify

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from im2webapp.models import (
    ImageModel,
    IntensityImageModifier,
    NoiseImageModifier,
    FilterImageModifier,
)


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = [
            'original_image',
            'name',
            'comments',
            'user',
        ]

    def clean(self):
        data = self.cleaned_data
        slug = slugify(data['name'])
        same_name_query = ImageModel.objects.filter(slug=slug, user=data['user'])
        
        if same_name_query.exists():
            raise ValidationError(_("Can't have duplicate image names"))


class AddIntensityModifierForm(forms.ModelForm):
    class Meta:
        model = IntensityImageModifier
        fields = [
            'type_of_modifier',
            'argument_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }

    def save(self, commit=True):
        m = super(AddIntensityModifierForm, self).save(commit=False)
        # Auto argument name
        if not m.argument_name:
            m.argument_name = (
                IntensityImageModifier.ARGUMENT_NAMES[m.type_of_modifier]
            )
        m.saved_name = str(m)
        if commit:
            m.save()
        return m


class AddNoiseModifierForm(forms.ModelForm):
    class Meta:
        model = NoiseImageModifier
        fields = [
            'noise_type',
            'argument1_value',
            'argument2_value',
            'amount_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }

    def save(self, commit=True):
        m = super(AddNoiseModifierForm, self).save(commit=False)
        # Auto argument name
        if not m.argument1_name:
            m.argument1_name = (
                NoiseImageModifier.ARGUMENT1_NAMES[m.noise_type]
            )
        if not m.argument2_name:
            m.argument2_name = (
                NoiseImageModifier.ARGUMENT2_NAMES[m.noise_type]
            )
        m.saved_name = str(m)
        if commit:
            m.save()
        return m


class AddFilterModifierForm(forms.ModelForm):
    class Meta:
        model = FilterImageModifier
        fields = [
            'filter_type',
            'filter_argument_value',
            'size_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }

    def save(self, commit=True):
        m = super(AddFilterModifierForm, self).save(commit=False)
        # Auto argument name
        if not m.filter_argument_name:
            m.filter_argument_name = (
                FilterImageModifier.ARGUMENT_NAMES[m.filter_type]
            )
        m.saved_name = str(m)
        if commit:
            m.save()
        return m
