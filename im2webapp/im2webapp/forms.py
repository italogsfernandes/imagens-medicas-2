from django import forms

from im2webapp.models import (
    ImageModel,
    ItensityImageModifier,
    NoiseImageModifier,
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
            'type_of_modifier': forms.HiddenInput(),
            'argument_name': forms.HiddenInput(),
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
