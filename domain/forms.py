from django import forms

class DomainForm(forms.Form):
    domain_list = ['.autos', '.boats', '.homes', '.yachts', '.motorcycles']
    domain = forms.CharField(label='Search Term', max_length=1000)
    extension = forms.CharField(label='Domain', max_length=30, widget=forms.Select(choices=domain_list))
