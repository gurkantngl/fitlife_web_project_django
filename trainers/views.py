from django.shortcuts import render, redirect, reverse
import pyrebase
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime

config = {
    
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

def trainerPanel(request):
    username = db.child("LoginningTrainer").child("username").get()
    username = username.val()
    
    if username == None:
        username = db.child("LoginningTrainer").get()
        username = username.val()
        username = username["username"]

    
    
    
    trainerList = db.child("TrainerLoginInfo").get()
    trainer = {}
    
    areas_of_expertise = db.child("Areas of Expertise").get()
    areas_of_expertise = [area for area in areas_of_expertise.val() if area is not None]
    
    for trainers in trainerList:
        if trainers.val() is not None:
            username2 = trainers.val()["username"]
            if username2 == username:
                trainer["id"] = trainers.val()["id"]
                trainer["username"] = trainers.val()["username"]
                trainer["name"] = trainers.val()["name"]
                trainer["surname"] = trainers.val()["surname"]
                trainer["password"] = trainers.val()["password"]
                trainer["email"] = trainers.val()["email"]
                try:
                    if type(trainers.val()["areas_of_experties"]) == dict:
                        trainers.val()["areas_of_experties"] = trainers.val()["areas_of_experties"].values()
                    trainer_experties = [area for area in trainers.val()["areas_of_experties"] if area is not None]
                except:
                    trainer_experties = []
    areas = [area for area in areas_of_expertise if area not in trainer_experties]         
    
    
    userList = db.child("UsersLoginInfo").get()
    clients = []
    
    for user in userList:
        try:
            if user.val()["trainer_username"] == trainer["username"]:
                clients.append(user.val())
        except:
            pass
    try:
        messageList = db.child("MessageUsers").child(trainer["username"]).get()
        
        messageList = messageList.val()
        messageList = messageList.values()
        messageList = list(messageList)
        
        for message in messageList:
            name = db.child("UsersLoginInfo").child(message["sender"]).child("name").get()
            name = name.val()
            surname = db.child("UsersLoginInfo").child(message["sender"]).child("surname").get()
            surname = surname.val()
            senderName = name + " " + surname
            message["senderName"] = senderName
    
    except:
        messageList = []        
    
    
    data = {
        "username": username,
        "trainer": trainer,
        "areas" : areas,
        "trainer_experties": trainer_experties,
        "clients" : clients,
        "messages" : messageList,
    }
    
    return render(request, 'CoachMain.html', data)


def updateProfile(request, trainer_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        db.child("LoginningTrainer").update({"username": username})
        
        data = {
            "name": name,
            "surname": surname,
            "email": email,
            "username": username,
        }
        
        db.child("TrainerLoginInfo").child(trainer_id).update(data)
        
        return redirect('trainerPanel')
    return redirect('trainerPanel')


def updateExpert(request, trainer_id):
    if request.method == 'POST':
        area = request.POST.get('uzmanlik_alani')
        print("area: ", area)
        db.child("TrainerLoginInfo").child(trainer_id).child("areas_of_experties").push(area)
        
        return redirect('trainerPanel')
    return redirect('trainerPanel')

def sendMessage(request, trainer_username):
    if request.method == 'POST':
        client = request.POST.get('client')
        message = request.POST.get('message')
        
        data = {
            "client": client,
            "message": message,
        }
        
        db.child("MessageTrainers").child(trainer_username).child(client).push(data)
        
        return redirect('trainerPanel')
    return redirect('trainerPanel')


def addNutritionProgram(request, client_id):
    
    data = {
        "client_id": client_id,
    }
    
    return render(request, 'AddNutrition.html', data)


def saveNutritionProgram(request, client_id):
    if request.method == 'POST':
        hedef = request.POST.get('hedef')
        kalori_hedef = request.POST.get('kalori')
        
        food1_1 = request.POST.get('food1-1')
        food1_2 = request.POST.get('food1-2')
        food1_3 = request.POST.get('food1-3')
        
        food2_1 = request.POST.get('food2-1')
        food2_2 = request.POST.get('food2-2')
        food2_3 = request.POST.get('food2-3')
        
        food3_1 = request.POST.get('food3-1')
        food3_2 = request.POST.get('food3-2')
        food3_3 = request.POST.get('food3-3')
        
        ogun_1 = {
            "yemek_1" : food1_1,
            "yemek_2" : food1_2,
            "yemek_3" : food1_3, 
        }
        
        ogun_2 = {
            "yemek_1" : food2_1,
            "yemek_2" : food2_2,
            "yemek_3" : food2_3,
        }
        
        ogun_3 = {
            "yemek_1" : food3_1,
            "yemek_2" : food3_2,
            "yemek_3" : food3_3,
        }
        
        data = {
            "hedef" : hedef,
            "kalori hedefi" : kalori_hedef,
            "Ogun1" : ogun_1,
            "Ogun2" : ogun_2,
            "Ogun3" : ogun_3,
        }
        
        db.child("UsersLoginInfo").child(client_id).child("nutrition_programs").set(data)
        
        return redirect("trainerPanel")
    return redirect("trainerPanel")

def viewNutritionProgram(request, client_id):
    nutirition_program = db.child("UsersLoginInfo").child(client_id).child("nutrition_programs").get()
    if nutirition_program is None:
        return redirect("trainerPanel")
        
    nutirition_program = nutirition_program.val()
    if nutirition_program is None:
        return redirect("trainerPanel")
    nutirition_program = nutirition_program.values()
    nutirition_program = list(nutirition_program)
    print(nutirition_program)
    
    kalori = nutirition_program[-1]
    nutirition_program.pop(-1)
    hedef = nutirition_program[-1]
    
    print(hedef)
    print(kalori)
    print(nutirition_program)
    
    data = {
        "hedef":hedef,
        "kalori":kalori,
        "program":nutirition_program,
    }
    
    return render(request, "viewNutritionProgram.html", data)


def addExerciseProgram(request, client_id):
    
    data = {
        "client_id": client_id,
    }
    
    return render(request, 'AddExercise.html', data)

def saveExerciseProgram(request, client_id):
    if request.method == 'POST':
        startDate = request.POST.get('start-date')
        startDate = datetime.strptime(startDate, '%Y-%m-%d')
        finishDate = request.POST.get('finish-date')
        finishDate = datetime.strptime(finishDate, '%Y-%m-%d')
        
        gunSayisi = (finishDate - startDate).days
        
        exercise1 = request.POST.get('exercise1')
        set1 = request.POST.get('set1')
        tekrar1 = request.POST.get('tekrar1')
        
        exercise2 = request.POST.get('exercise2')
        set2 = request.POST.get('set2')
        tekrar2 = request.POST.get('tekrar2')
        
        exercise3 = request.POST.get('exercise3')
        set3 = request.POST.get('set3')
        tekrar3 = request.POST.get('tekrar3')
        
        exercise4 = request.POST.get('exercise4')
        set4 = request.POST.get('set4')
        tekrar4 = request.POST.get('tekrar4')
        
        exercise5 = request.POST.get('exercise5')
        set5 = request.POST.get('set5')
        tekrar5 = request.POST.get('tekrar5')
        
        data = {
            "baslangic_tarihi" : str(startDate),
            "bitis_tarihi" : str(finishDate),
            "gun_sayisi" : gunSayisi,
            "exercise1" : exercise1,
            "set1" : set1,
            "tekrar1" :tekrar1,
            "exercise2" : exercise2,
            "set2" : set2,
            "tekrar2" :tekrar2,
            "exercise3" : exercise3,
            "set3" : set3,
            "tekrar3" :tekrar3,
            "exercise4" : exercise4,
            "set4" : set4,
            "tekrar4" : tekrar4,
            "exercise5" : exercise5,
            "set5" : set5,
            "tekrar5" : tekrar5,           
        }
        
        db.child("UsersLoginInfo").child(client_id).child("exercise_program").set(data)
        
        return redirect("trainerPanel")
    return redirect("trainerPanel")

def viewExerciseProgram(request, client_id):
    exercise_program = db.child("UsersLoginInfo").child(client_id).child("exercise_program").get()
    
    if exercise_program is None:
        return redirect("trainerPanel")
    
    exercise_program = exercise_program.val()
    print(exercise_program["tekrar2"])
    print("-------")
    exercise_program2 = exercise_program.values()
    print(exercise_program)
    print("--------------------------------")
    exercise_program2 = list(exercise_program2)
    
    gun_sayisi = exercise_program2[7]
    exercise_program2.pop(7)
    
    print(exercise_program)
    print(gun_sayisi)
    
    data = {
        "gun_sayisi": gun_sayisi,
        "program" : exercise_program,
    }
    
    return render(request, "viewExerciseProgram.html", data)

def deleteExerciseProgram(request, client_id):
    db.child("UsersLoginInfo").child(client_id).child("exercise_program").remove()
    
    return redirect("trainerPanel")

def deleteNutritionProgram(request, client_id):
    db.child("UsersLoginInfo").child(client_id).child("nutrition_programs").remove()
    
    return redirect("trainerPanel")