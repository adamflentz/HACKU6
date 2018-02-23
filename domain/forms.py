from django import forms

class DomainForm(forms.Form):
    extension_list = [('.autos', '.autos'), ('.boats', '.boats'), ('.homes', '.homes'), ('.yachts', '.yachts'), ('.motorcycles', '.motorcycles')]
    domain = forms.CharField(label='Search Term', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'size':50}))
    extension = forms.ChoiceField(label='Domain', choices=extension_list, widget=forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle'}))
