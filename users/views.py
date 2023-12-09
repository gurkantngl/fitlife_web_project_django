from django.shortcuts import render, redirect, reverse
import pyrebase
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import UpdateForm

config = {
    
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@csrf_exempt
def userPanel(request):
    email = db.child("LoginningUser").child("email").get()
    email = email.val()
    
    print("email: ", email)
    userList = db.child("UsersLoginInfo").get()
    user = {}
    
    for users in userList:
        if users.val()["email"] == email:
            user["id"] = users.val()["id"]
            user["name"] = users.val()["name"]
            user["surname"] = users.val()["surname"]
            user["password"] = users.val()["password"]
            user["email"] = users.val()["email"]
            user["telefon"] = users.val()["telefon"]
            user["cinsiyet"] = users.val()["cinsiyet"]
            user["dogum_tarihi"] = users.val()["dogum_tarihi"]
            user["trainer_username"] = users.val()["trainer_username"]
            try:
                user["kilo"] = users.val()["body_infos"]["kilo"]
                user["boy"] = users.val()["body_infos"]["boy"]
                user["yag"] = users.val()["body_infos"]["yag"]
                user["kitle_endeksi"] = users.val()["body_infos"]["kitle_endeksi"]
            except:
                pass
    print("user_id: ", user["id"])
        
    file_name = user["id"]
    img_name = file_name + ".jpg"
    print("file_name: ", file_name)
    
    storage.child(file_name).download("", f"./static/{img_name}")
    
    try:
        messageList = db.child("MessageTrainers").child(user["trainer_username"]).get()
        messageList = messageList.val()[user["name"] + " " + user["surname"]]
        messageList = messageList.values()
        messageList = list(messageList)
        
        print("messageList: ", messageList)
        print(type(messageList))
        
        
        messages = []
        for message in messageList:
            if message["client"] == user["name"] + " " + user["surname"]:
                messages.append(message)
    
    except:
        messages = []
    
    
    nutrition_program = db.child("UsersLoginInfo").child(user["id"]).child("nutrition_programs").get()
    nutrition_program = nutrition_program.val()
    if nutrition_program is not None:
        nutrition_program = nutrition_program.values()
        nutrition_program = list(nutrition_program)
        print(nutrition_program)
    
        kalori = nutrition_program[-1]
        nutrition_program.pop(-1)
        hedef = nutrition_program[-1]
    
    else:
        kalori = 0
        hedef = 0
    
    exercise_program = db.child("UserLoginInfo").child(user["id"]).child("exercise_program").get()
    
    
    exercise_program = exercise_program.val()
    if exercise_program is not None:
        exercise_program2 = exercise_program.values()
        exercise_program2 = list(exercise_program2)
        
        startDate = exercise_program2[0]
        finishDate = exercise_program2[1]
    
    else:
        startDate = 0
        finishDate = 0
    
    
    data = {"email": email,
            "img_name": img_name,
            "user" : user,
            "messages" : messages,
            "kalori" : kalori,
            "hedef" : hedef,
            "startDate" : startDate,
            "finishDate" : finishDate,
            }
    
    return render(request, 'UserMain.html', data)



def update(request, user_id):
    
    if request.method == "POST":
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        #profil_resmi = request.POST.get('profile-image')
        
        db.child("LoginningUser").update({"email" : email})
        #print("Profil Resmi: ", profil_resmi)
        #storage.child(user_id).put(profil_resmi)
        #profil_url = storage.child(user_id).get_url(None)
        
        data = {
            "name": name,
            "surname": surname,
            "dogum_tarihi" : str(birth_date),
            "cinsiyet" : gender,
            "email" : email,
            "telefon" : phone,
            #"profil_url" : profil_url,
        }
        
        db.child("UsersLoginInfo").child(user_id).update(data)
        
        return redirect("userPanel")
    return redirect("userPanel")


def sendMessageUser(request, user_id):
    if request.method == "POST":
        trainer_username = request.POST.get('trainer')
        message = request.POST.get('message')
        
        data = {
            "sender" : user_id,
            "message" : message,
        }
        
        db.child("MessageUsers").child(trainer_username).push(data)
        
        return redirect("userPanel")
    return redirect("userPanel")

def viewNutritionProgramUser(request, client_id):
    nutrition_program = db.child("UserLoginInfo").child(client_id).child("nutrition_programs").get()
    
    if nutrition_program is None:
        return redirect('userPanel')
    
    nutrition_program = nutrition_program.val()
    
    if nutrition_program is None:
        return redirect('userPanel')
    
    nutrition_program = nutrition_program.values()
    nutrition_program = list(nutrition_program)
    
    kalori = nutrition_program[-1]
    nutrition_program.pop(-1)
    hedef = nutrition_program[-1]
    
    data = {
        "hedef" : hedef,
        "kalori" : kalori,
        "program" : nutrition_program
    }

    return render(request, "viewNutritionProgram.html", data)

def viewExerciseProgramUser(request, client_id):
    exercise_program = db.child("UsersLoginInfo").child(client_id).child("exercise_program").get()
    
    if exercise_program is None:
        return redirect("userPanel")
    
    exercise_program = exercise_program.val()
    if exercise_program is None:
        return redirect("userPanel")
    exercise_program2 = exercise_program.values()
    exercise_program2 = list(exercise_program2)
    
    gun_sayisi = exercise_program2[7]
    exercise_program2.pop(7)
    
    data = {
        "gun_sayisi": gun_sayisi,
        "program": exercise_program,
        "client_id": client_id,
    }
    
    return render(request, "UserExercise.html", data)
    
def updateInfo(request, client_id):
    if request.method == "POST":
        kilo = request.POST.get("kilo")
        boy = request.POST.get("boy")
        yag = request.POST.get("yag_orani")
        
        kitle_endeksi = float(kilo) / (float(boy)**2)
        
        data = {
            "kilo" : kilo,
            "boy" : boy,
            "yag" : yag,
            "kitle_endeksi" : str(kitle_endeksi)
        }  
        db.child("UsersLoginInfo").child(client_id).child("body_infos").set(data)
    return redirect("userPanel")

def updateExerciseProgram(request, client_id, gun_sayisi):
    if request.method == "POST":
        print("post")
        print("gun_sayisi: ", gun_sayisi)
        counter=0
        for i in range(gun_sayisi):
            gun = request.POST.get('agree '+str(i+1))
            print("gun: ", gun)
            if gun is not None:
                counter+=1
        db.child("UsersLoginInfo").child(client_id).child("programCounter").set(counter) 
    return redirect('userPanel')
            
    