from django import forms

from im2webapp.models import (
    ImageModel,
    ItensityImageModifier,
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


class AddIntensityModifierForm(forms.ModelForm):
    class Meta:
        model = ItensityImageModifier
        fields = [
            'type_of_modifier',
            'argument_name',
            'argument_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }


class AddNoiseModifierForm(forms.ModelForm):
    class Meta:
        model = NoiseImageModifier
        fields = [
            'noise_type',
            'argument1_name',
            'argument1_value',
            'argument2_name',
            'argument2_value',
            'amount_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }


class AddFilterModifierForm(forms.ModelForm):
    class Meta:
        model = FilterImageModifier
        fields = [
            'filter_type',
            'argument1_name',
            'argument1_value',
            'argument2_name',
            'argument2_value',
            'amount_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }
