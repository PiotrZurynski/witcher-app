from django import forms
from .models import Contract

class ContractCreateForm(forms.ModelForm):
    class Meta:
        model=Contract
        fields=('title','description','realm','town','monster','currency','reward')
        exclude=['owner, time_created']
        