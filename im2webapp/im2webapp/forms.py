from django import forms

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
        if commit:
            m.save()
        return m


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
            'size_value',
            'imagem'
        ]
        widgets = {
            'imagem': forms.HiddenInput(),
        }
