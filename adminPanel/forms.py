from django import forms

class UserRegisterForm(forms.Form):
    name = forms.CharField(max_length=40, label = "Ad")
    surname = forms.CharField(max_length=40, label = "Soyad")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula",widget=forms.PasswordInput)
    cinsiyet = forms.ChoiceField(choices=[('', 'Cinsiyet Seçiniz'), ('erkek', 'Erkek'), ('kadın', 'Kadın')],
                                widget=forms.Select(attrs={'required': 'required'}))
    email = forms.EmailField(label='E-posta Adresi', widget=forms.EmailInput(attrs={'placeholder': 'E-posta Adresi', 'required': 'required'}))
    telefon = forms.CharField(label='Telefon Numarası', widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefon Numarası', 'required': 'required'}))
    dogum_tarihi = forms.DateField(label='Doğum Tarihi', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Doğum Tarihi', 'required': 'required'}))
    
    hedefler = [
        ('Kilo Alma', 'Kilo Alma'),
        ('Kilo Verme', 'Kilo Verme'),
        ('Kiloyu Koruma', 'Kiloyu Koruma'),
        ('Kas Kazanma', 'Kas Kazanma'),
    ]
    
    hedef = forms.ChoiceField(choices=hedefler, label='Hedef')
    
    
class TrainerRegisterForm(forms.Form):
    name = forms.CharField(max_length=40, label = "Ad")
    surname = forms.CharField(max_length=40, label = "Soyad")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula",widget=forms.PasswordInput)
    email = forms.EmailField(label='E-posta Adresi', widget=forms.EmailInput(attrs={'placeholder': 'E-posta Adresi', 'required': 'required'}))
