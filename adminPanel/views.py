from django.shortcuts import render, redirect
import pyrebase
from .forms import UserRegisterForm, TrainerRegisterForm


config = {
    
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

def adminPanel(request):
    return render(request, 'AdminMain.html')



def users(request):
    form = UserRegisterForm(request.POST or None)
    userList = db.child("UsersLoginInfo").get()
    print(userList.val())
    if form.is_valid():
        cleaned_data = form.cleaned_data
        email = cleaned_data['email']
        userList = db.child("UsersLoginInfo").get()
        emailList = [user.val()["email"] for user in userList]
        
        if email not in emailList:
            name = cleaned_data['name']
            surname = cleaned_data['surname']
            password = cleaned_data['password']
            cinsiyet = cleaned_data['cinsiyet']
            email = cleaned_data['email']
            telefon = cleaned_data['telefon']
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
            print("user_id: " + user_id)
            db.child("UsersLoginInfo").child(user_id).child("id").set(user_id)
            
            return redirect('users')

        else:
            print("Bu e-posta zaten kayıtlı")
            userList2 = []
            for user in userList:
                if user.val() is not None:
                    userList2.append(user.val())
            
            context = {
                "form" : form,
                "userList" : userList2,
            }    
            
            return render(request, 'AdminUser.html', context)
        
        
        
    userList2 = []
    for user in userList:
        if user.val() is not None:
            userList2.append(user.val())
    
    
    context = {
        "form" : form,
        "userList" : userList2,
    }    
    
    return render(request, 'AdminUser.html', context)



def trainers(request):
    form = TrainerRegisterForm(request.POST or None)
    trainerList = db.child("TrainerLoginInfo").get()
    if form.is_valid():
        cleaned_data = form.cleaned_data
        email = cleaned_data["email"]
        trainerList = db.child("TrainerLoginInfo").get(),
        try:
            emailList = [trainer.val()["email"] for trainer in trainerList]
            print("emailList: ", emailList)
        except:
            emailList = []
        
        if email not in emailList:
        
            name = cleaned_data['name']
            surname = cleaned_data['surname']
            password = cleaned_data['password']
            
            
            data = {
                "name" : name,
                "surname" : surname,
                "password" : password,
                "email" : email,
                "is_active" : True,
                "number_of_clients" : 0,
            }
            
            trainer_id = db.child("TrainerLoginInfo").push(data)
            trainer_id = trainer_id["name"]
            db.child("TrainerLoginInfo").child(trainer_id).child("id").set(trainer_id)
            print("Başarıyla kayıt oluşturuldu...")

            return redirect('trainers')

        else:
            print("Bu e-mail zaten kayıtlı")
            trainerList2 = []
            for trainer in trainerList:
                if trainer.val() is not None:
                    trainerList2.append(trainer.val())
            
            context = {
                "form" : form,
                "trainerList" : trainerList2
            }
            
            return render(request, 'AdminCoach.html', context)
        
    trainerList2 = []
    for trainer in trainerList:
        if trainer.val() is not None:
            trainerList2.append(trainer.val())
    
    context = {
        "form" : form,
        "trainerList" : trainerList2,
    }
        
    return render(request, 'AdminCoach.html', context)


def trainerActivePassive(request, trainer_email):
    trainerList = db.child("TrainerLoginInfo").get()
    for trainer in trainerList:
            if trainer.val() is not None and trainer.val()["email"] == trainer_email:
                trainer_id =  trainer.val()["id"]
                is_active = trainer.val()["is_active"]
                db.child("TrainerLoginInfo").child(trainer_id).child("is_active").set(not is_active)
                break
    return redirect("trainers")


def userActivePassive(request, user_email):
            
    userList = db.child("UsersLoginInfo").get()
    for user in userList:
        if user.val()["email"] == user_email:
            user_id = user.val()["id"]
            is_active = user.val()["is_active"]
            db.child("UsersLoginInfo").child(user_id).child("is_active").set(not is_active)
            break
    return redirect("users")


def userUpdate(request, user_id):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        userList = db.child("UsersLoginInfo").get()
        print("userList.val(): ",userList.val())
        for user in userList:
            if user.val() is not None:
                if user.val()["id"] == user_id:
                    data = {
                        "name" : name,
                        "surname" : surname,
                        "dogum_tarihi" : str(birth_date),
                        "cinsiyet" : gender,
                        "email" : email,
                        "telefon" : phone,
                    }
                    
                    db.child("UsersLoginInfo").child(user_id).update(data)
        return redirect("users")
                    
    return redirect("users")


def trainerUpdate(request, trainer_id):
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
      
        
        trainerList = db.child("TrainerLoginInfo").get()
        for trainer in trainerList:
            if trainer.val() is not None:
                if str(trainer.val()["id"]) == str(trainer_id):
                    data = {
                        "name" : name,
                        "surname" : surname,
                        "email" : email,
                    }
                    db.child("TrainerLoginInfo").child(trainer_id).update(data)
        return redirect("trainers")
    return redirect("trainers")