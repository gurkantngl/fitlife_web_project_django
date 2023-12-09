from django.shortcuts import render, redirect
from .forms import RegisterForm, UserLoginForm, LoginForm, ForgetPasswordForm, ResetPasswordForm, ConfirmCodeForm
import pyrebase
from django.contrib.auth.models import User
from django.contrib import messages
from .helpers import send_forget_password_mail
import random
import requests
import json

config = {

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def index(request):
    return render(request, 'index.html')



def loginPanelAdmin(request):
    
    form = LoginForm(request.POST or None)
    
    if form.is_valid():
        
        cleaned_data = form.cleaned_data
        
        username = cleaned_data['username']
        password = cleaned_data['password']
        
        confirm_username = db.child("AdminLoginInfo").child("username").get()
        confirm_password = db.child("AdminLoginInfo").child("password").get()
        
        if str(confirm_username.val()) == str(username) and str(confirm_password.val()) == str(password):
            messages.info(request,"Başarı ile Giriş Yaptınız...")
            print("Başarı ile Giriş Yaptınız")
            return redirect("adminPanel")
        
        print("Giriş Yapılamadı")
        return redirect("loginAdmin")
    
    context = {
        "form" : form
    }
    return render(request,'admin-login.html', context)


    
def loginPanelTrainer(request):
    form = LoginForm(request.POST or None)
    
    if form.is_valid():
        
        cleaned_data = form.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password']
        trainers = db.child("TrainerLoginInfo").get()
        trainers = trainers.val()
        for trainer in trainers:
            if trainer is not None:
                print("trainer: ", trainer)
                confirm_username = trainer["username"]
                confirm_password = trainer["password"]
                is_active = trainer["is_active"]
                
                if is_active == False:
                    return render(request, 'coach-login.html')
                
                print("confirm_username: ", confirm_username)
                print("confirm_password: ", confirm_password)
                
                if str(confirm_username) == str(username) and str(confirm_password) == str(password):
                    messages.info(request,"Başarı ile Giriş Yaptınız...")
                    print("Başarı ile Giriş Yaptınız")
                    
                    db.child("LoginningTrainer").child("username").set(username)
                    
                    return redirect("trainerPanel")
    
        print("Giriş Yapılamadı")
        return redirect("loginTrainer")
    
    context = {
        "form" : form
    }
    return render(request,'coach-login.html', context)





def loginPanelUser(request):
    form = UserLoginForm(request.POST or None)
    
    if form.is_valid():
        
        cleaned_data = form.cleaned_data
        
        email = cleaned_data['email']
        password = cleaned_data['password']
        
        userList = db.child("UsersLoginInfo").get()
        
        user_id = 0
        for user in userList:
            if user.val()["email"] == email:
                user_id = user.val()["id"]
                user_is_active = user.val()["is_active"]
        
        if user_is_active == False:
            return render(request, 'member-login.html')

        confirm_email = db.child("UsersLoginInfo").child(user_id).child("email").get()
        confirm_password = db.child("UsersLoginInfo").child(user_id).child("password").get()
        
        
        if confirm_email.val() == email and confirm_password.val() == password:
            messages.info(request,"Başarı ile Giriş Yaptınız...")
            print("Başarı ile Giriş Yaptınız")
            
            db.child("LogginningUser").remove()
            db.child("LoginningUser").child("email").set(email)
            
            return redirect("userPanel")
        
        print("Giriş Yapılamadı")
        return redirect("loginUser")
    
    context = {
        "form" : form
    }
    return render(request,'member-login.html', context)




def forgetpassword(request):
    form = ForgetPasswordForm(request.POST or None)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        email = cleaned_data['email']
        key = email.split('@')[0]
        confirm_email = db.child("UsersLoginInfo").child(key).child("email").get()
    
        if confirm_email.val() == email:
             
            print("Email gönderiliyor...")
            code = random.randint(1000, 9999)
            send_forget_password_mail(email, code)
            print("Email gönderildi!")
            db.child("resetcode").remove()
            db.child("resetcode").child("email").set(email)
            db.child("resetcode").child("code").set(code)
            
            context = {
                "email": email,
            }
            
            return redirect("confirmcode")
        
        print("ife girmedi")
        messages.info(request, "Kayıt Bulunamadı...")
        return redirect("forgetpassword")
    
    context = {
        "form" : form
    }
    
    return render(request, 'forget-password.html', context)




def confirmcode(request):
    form = ConfirmCodeForm(request.POST or None)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        
        confirmcode = cleaned_data['code']
        confirm_code = db.child("resetcode").child("code").get()
        
        print(confirmcode)
        print(confirm_code.val())
        
        if str(confirmcode) == str(confirm_code.val()):       
            messages.info(request,"Başarı ile Giriş Yaptınız...")
            print("Başarı ile Giriş Yaptınız")
            return redirect("changepassword")
        
        print("Giriş Yapılamadı")
        context = {
            "form" : form,
        }
        return render(request,'confirmcode.html', context)
    
    context = {
            "form" : form,
    }
    return render(request,'confirmcode.html', context)




def changepassword(request):
    form = ResetPasswordForm(request.POST or None)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        
        if password == confirm_password:
            email = db.child("resetcode").child("email").get()
            key = email.val().split('@')[0]
            db.child("UsersLoginInfo").child(key).child("password").set(password)
            return redirect('loginUser')

        context = {
            "form" : form,
        }
        
        return render(request, "reset-password.html", context)

    context = {
        "form" : form,
    }
   
    return render(request, "reset-password.html", context)
    



def registerpanel(request):
    
    form = RegisterForm(request.POST, request.FILES or None)
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        email = cleaned_data['email']
        userList = db.child("UsersLoginInfo").get()
        try:
            emailList = [user.val()["email"] for user in userList]
        except :
            emailList = []
        
        if email not in emailList:
            name = cleaned_data['name']
            surname = cleaned_data['surname']
            password = cleaned_data['password']
            cinsiyet = cleaned_data['cinsiyet']
            
            telefon = cleaned_data['telefon']
            profil_resmi = cleaned_data['profil_resmi']
            dogum_tarihi = cleaned_data['dogum_tarihi']
            hedef = cleaned_data['hedef']
        
            
            trainer_username = ""
            trainerList = db.child("TrainerLoginInfo").get()
            for trainer in trainerList:
                if trainer.val() is not None:
                    number = int(trainer.val()["number_of_clients"])
                    print("Number: ", number)
                    
                    areas = trainer.val()["areas_of_experties"]
                    areas = list(areas.values())
                    print("areas: ", areas)
                    
                    if hedef in areas and number < 5:
                        print("id: ",trainer.val()["id"])
                        db.child("TrainerLoginInfo").child(str(trainer.val()["id"])).update({"number_of_clients" : (number+1)})
                        trainer_username = trainer.val()["username"]
                        break
            
            if len(trainer_username) == 0:
                for trainer in trainerList:
                    if trainer.val() is not None:
                        number = int(trainer.val()["number_of_clients"])
                        print("Number: ", number)
                        
                        if number < 5:             
                            db.child("TrainerLoginInfo").child(str(trainer.val()["id"])).update({"number_of_clients" : (number+1)})
                            trainer_username = trainer.val()["username"]
                            break
            
            data = {
                    "name" : name,
                    "surname" : surname,
                    "password" : password,
                    "cinsiyet" : cinsiyet,
                    "telefon" : telefon,
                    "email" : email,
                    "dogum_tarihi" : str(dogum_tarihi),
                    "is_active" : True,
                    "hedef" : hedef,
                    "trainer_username" : trainer_username,
                }
            
            print("Başarıyla kayıt oluşturuldu..")
            user_id = db.child("UsersLoginInfo").push(data)
            user_id = user_id["name"]
            print("Profil Resmi: ",profil_resmi)
            storage.child(user_id).put(profil_resmi)
            profil_url = storage.child(user_id).get_url(None)
            db.child("UsersLoginInfo").child(user_id).child("profil_url").set(profil_url)
            db.child("UsersLoginInfo").child(user_id).child("id").set(user_id)
            
            return redirect('loginUser')

        else:
            messages.info(request,"Bu e-posta kayıtlı...")
            context = {
                "form" : form
            }
            return render(request,'member-register.html', context)
        
    context = {
        "form" : form
    }
    return render(request,'member-register.html', context)