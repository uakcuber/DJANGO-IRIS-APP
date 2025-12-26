from django import forms
from .models import IrisPlant


class IrisPlantForm(forms.ModelForm):
    # Modelde 'choices'ı kaldırdığımız için, Dropdown seçeneklerini burada elle tanımlıyoruz.
    SPECIES_CHOICES = [
        ('Iris-setosa', 'Iris-setosa'),
        ('Iris-versicolor', 'Iris-versicolor'),
        ('Iris-virginica', 'Iris-virginica'),
    ]

    # Species alanını override ediyoruz: Hem dropdown olsun hem de CSS sınıfı alsın
    species = forms.ChoiceField(
        choices=SPECIES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tür"
    )

    class Meta:
        model = IrisPlant
        fields = ['location', 'species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width']

        widgets = {
            # Location (ForeignKey) otomatik dropdown olur ama stil ekliyoruz
            'location': forms.Select(attrs={'class': 'form-control'}),

            # Sayısal alanlar
            'sepal_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'sepal_width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'petal_length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'petal_width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }