from django import forms


class FastMedisinForm(forms.Form):
    diagnose                = forms.CharField(label='Diagnose',
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'Hjerteinfarkt'"}))
    cave                    = forms.CharField(label='CAVE',
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'Penicillin'"}))
    ny_medisin              = forms.BooleanField(label='Ny medisin?',
                                                required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'ny_medisin'}))
    legemiddelnavn          = forms.CharField(label='Legemiddelnavn',                                                
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'Paracet'"}))
    legemiddelform          = forms.CharField(label='Legemiddelform',
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'tbl'"}))
    enhet                   = forms.CharField(label='Enhet',            
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'mg'"}))
    administrasjonsform     = forms.CharField(label='Administrasjon',   
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'medisin', 'placeholder': "f eks 'p.o.'"}))

    dose0008                = forms.CharField(label='Dose',
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'dose', 'placeholder': "kl 00-08."}))
    dose1420                = forms.CharField(label='',
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'dose', 'placeholder': "kl 14-20."}))
    dose0814                = forms.CharField(label='', 
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'dose', 'placeholder': "kl 08-14."}))
    dose2024                = forms.CharField(label='', 
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'dose', 'placeholder': "kl 20-24."}))
    dose_fritekst           = forms.CharField(label='', 
                                                required=False,
                                                widget=forms.TextInput(attrs={'class': 'dose', 'placeholder': "f eks '10mg inntil x 3"}))
    notat                   = forms.CharField(label='Notater', 
                                                required=False,
                                                widget=forms.Textarea(attrs={'class': 'notat', 'rows': '15', 'cols': '50', 'wrap': 'hard', 'placeholder': "Skriv notater her."}))
    autofill_faste          = forms.CharField(label='Faste medisiner', 
                                                required=False,
                                                widget=forms.Textarea(attrs={'class': 'autofill', 'rows': '20', 'cols': '50', 'wrap': 'hard', 'placeholder': "Kopier inn faste medisiner her"}))
    autofill_behov          = forms.CharField(label='Eventulle medisiner', 
                                                required=False,
                                                widget=forms.Textarea(attrs={'class': 'autofill', 'rows': '20', 'cols': '50', 'wrap': 'hard', 'placeholder': "Kopier inn behovs-medisiner her"}))








