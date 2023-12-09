from django import forms

class UpdateForm(forms.Form):
    name = forms.CharField(max_length=40, label = "Ad", required=False)
    surname = forms.CharField(max_length=40, label = "Soyad", required=False)
    password = forms.CharField(max_length=20, label="Parola", required=False, widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula", required=False, widget=forms.PasswordInput)
    cinsiyet = forms.ChoiceField(choices=[('', 'Cinsiyet Seçiniz'), ('erkek', 'Erkek'), ('kadın', 'Kadın')],
                                widget=forms.Select(attrs={}), required=False)
    email = forms.EmailField(label='E-posta Adresi', widget=forms.EmailInput(attrs={'placeholder': 'E-posta Adresi'}), required=False)
    telefon = forms.CharField(label='Telefon Numarası', widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefon Numarası'}), required=False)
    
    profil_resmi = forms.ImageField(label='Profil Resmi', required=False)
    print(type(profil_resmi))
    dogum_tarihi = forms.DateField(label='Doğum Tarihi', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Doğum Tarihi'}), required=False)
    