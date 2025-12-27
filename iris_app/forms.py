from django import forms
from .models import IrisPlant


class IrisPlantForm(forms.ModelForm):
    SPECIES_CHOICES = [
        ('Iris-setosa', 'Iris-setosa'),
        ('Iris-versicolor', 'Iris-versicolor'),
        ('Iris-virginica', 'Iris-virginica'),
    ]

    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tür"
    )

    class Meta:
        model = IrisPlant
        fields = ['location', 'species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width']

        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),

            # Sayısal alanlar
            'sepal_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'sepal_width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'petal_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'petal_width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Location alanı zorunlu
        self.fields['location'].required = True
        self.fields['location'].empty_label = "-- Konum Seçin --"