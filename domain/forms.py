from django import forms

class DomainForm(forms.Form):
    domain_list = [('1', '.autos'), ('2', '.boats'), ('3', '.homes'), ('4', '.yachts'), ('5', '.motorcycles')]
    domain = forms.CharField(label='Search Term', max_length=1000)
    extension = forms.ChoiceField(label='Domain', choices=domain_list)
