from django import forms


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=40, label="E-Mail")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)

class ForgetPasswordForm(forms.Form):
    email = forms.CharField(max_length=40, label="E-Mail")

class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=40, label="Doğrulama Kodu")
    confirmcode = int()

class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=50, label="Parola", widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, label="Parolayı Onayla", widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, label="Kullanıcı Adı")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=40, label = "Ad")
    surname = forms.CharField(max_length=40, label = "Soyad")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula",widget=forms.PasswordInput)
    cinsiyet = forms.ChoiceField(choices=[('', 'Cinsiyet Seçiniz'), ('erkek', 'Erkek'), ('kadın', 'Kadın')],
                                widget=forms.Select(attrs={'required': 'required'}))
    email = forms.EmailField(label='E-posta Adresi', widget=forms.EmailInput(attrs={'placeholder': 'E-posta Adresi', 'required': 'required'}))
    telefon = forms.CharField(label='Telefon Numarası', widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Telefon Numarası', 'required': 'required'}))
    
    profil_resmi = forms.ImageField(label='Profil Resmi', required=False)
    print(type(profil_resmi))
    dogum_tarihi = forms.DateField(label='Doğum Tarihi', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Doğum Tarihi', 'required': 'required'}))
    
    hedefler = [
        ('Kilo Alma', 'Kilo Alma'),
        ('Kilo Verme', 'Kilo Verme'),
        ('Kiloyu Koruma', 'Kiloyu Koruma'),
        ('Kas Kazanma', 'Kas Kazanma'),
    ]
    
    hedef = forms.ChoiceField(choices=hedefler, label='Hedef')
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        return cleaned_data
    