from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np
from . import forms
from django.contrib.auth import login
from .request.Request_BDD import Request_BDD
from .faceNet_models.code.real_time_face_recognition import run_predictions
import argparse
import sys
import time
from popit_app.faceNet_models.code import face
from popit_app.faceNet_models.code.real_time_face_recognition import add_overlays


def gen(type_):
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    video_capture = cv2.VideoCapture(0)
    if type_ == 1:
        face_recognition = face.Recognition()
    start_time = time.time()

    """  
    if args.debug:
        print("Debug enabled")
        face.debug = True
    """
    while True:
        
        # Capture frame-by-frame
        if type_ == 0:
            ret, frame = video_capture.read()
            #frame_flip = cv2.flip(frame, 1)
            ret, frame = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

        if type_ == 1:
            ret, frame = video_capture.read()
            l_names = None 
            if (frame_count % frame_interval) == 0:
                faces,l_names = face_recognition.identify(frame)
                #print(l_names)
                # Check our current fps
                end_time = time.time()
                if (end_time - start_time) > fps_display_interval:
                    frame_rate = int(frame_count / (end_time - start_time))
                    start_time = time.time()
                    frame_count = 0

            add_overlays(frame, faces, frame_rate)
            frame_count += 1
            ret, frame = cv2.imencode('.jpg', frame)
            
            try:
                name = l_names[0]
                yield (name+"_")
            except:
                name = "/"
            
                
            #yield l_names
            #yield (name+"_")

def video_stream(request,type_):
    video_object=gen(type_)
    content_type = 'multipart/x-mixed-replace; boundary=frame'
    if type_ == 1:
        content_type = 'text/event-stream'

    return StreamingHttpResponse(video_object,content_type=content_type)

  
def game(request):
    return render(request,"game.html")



#CHECK SESSION
def checkSession(request):
    try:
        nom = request.session['nom']
    except:
        nom = ""
    return nom

def verifyAuth(request):
    try:
        auth = request.session['auth']
    except:
        auth = False
    return auth   



def checkAuth(request):
    
    if request.method =="POST":
        value = request.POST.get("checkAuth")
        if value == "0":
            return redirect("jouer")

        else:
            request.session["auth"] = True
            return redirect("game2")

    else:
        return redirect('accueil')

# ARCHITECTURE APPLICATION    

def gamefinal(request):
    nom = checkSession(request)
    return render(request,"gamefinal.html",{'nom':nom})

def accueil(request):
    #Request_BDD.addModele('PopIt/popit_django/popit_app/faceNet_models/testModels.h5')
    #Request_BDD.addMode('classique', 'facile', 180, False)
    #Request_BDD.addMode('classique', 'moyen', 240, False)
    #Request_BDD.addMode('classique', 'difficile', 300, False)
    #Request_BDD.addMode('explosif', 'facile', 180, True)
    #Request_BDD.addMode('explosif', 'difficile', 300, True)

    nom = checkSession(request)
    return render(request,"accueil.html",{'nom':nom})

def inscription(request):
    nom = checkSession(request)
    form =  forms.inscription_form()
    if request.method == "POST":
        form = forms.inscription_form(request.POST)
        
        if form.is_valid():
            infos = request.POST
            if ((infos['password'] == infos['password2']) and (Request_BDD.verifyDisponiblePseudo(infos['pseudo']) == 0)):
                Request_BDD.inscription(infos['email'], infos['nom'], infos['prenom'], infos['password'], infos['pays'], infos['pseudo'])
                return redirect(connexion)
            else :
                return render(request, "inscription.html", {'form' : form, 'nom':nom})

    form = forms.inscription_form()
    return render(request, "inscription.html", {'form' : form, 'nom':nom})

def connexion(request):
    nom = checkSession(request)
    form = forms.connexion_form()
    if request.method == "POST":
        if request.POST.get('email', default=None) is None:
            return render(request,"connexion.html", {'form' : form, 'nom':nom})

        form = forms.connexion_form(request.POST)
        if form.is_valid():
            infos = request.POST
            validation = Request_BDD.connexion(infos['email'], infos['password'])

            if validation == True:
                nomJoueur = Request_BDD.getNomJoueur(infos['email'])
                request.session['nom'] = nomJoueur
                request.session['mail'] = infos['email']
                request.session['auth'] = False

                return redirect(accueil)
            else:
                return render(request,"connexion.html", {'form' : form, 'nom':nom})
 
    else:
        return render(request,"connexion.html", {'form' : form, 'nom':nom})

def deconnexion(request):
    if request.method == "POST":
        try:
            del request.session['nom']
            del request.session['mail']
        except:
            pass
        
    nom = checkSession(request)
    return redirect('accueil')

def getDifficultes(request):
    if request.method == "POST":
        mode = request.POST.get('mode')
        difficultes = Request_BDD.getDifficultes(mode)
        response_data = {
            "difficultes": difficultes
        }
        return JsonResponse(response_data)


def jouer(request):
    nom = checkSession(request)
    modes = Request_BDD.getMode()
    return render(request,"jouer.html",{'nom':nom, 'modes': modes})

def classement(request):
    nom = checkSession(request)
    try:
        lastGame = Request_BDD.getLastGame(request.session['mail'])

        # section historique
        columnNamesHisto = ['Date', 'Durée', 'Nom du mode', 'Difficulte du mode', 'Score']
        historiqueParties = Request_BDD.getHistoriquePerso(request.session['mail'])

        # section classement
        columnNamesClass = ['Joueur','Date', 'Durée', 'Nom du mode', 'Difficulte du mode','Score']
        classementParties = Request_BDD.getClassement()

        return render(request,"classement.html",{'nom':nom,
                                                'score': lastGame.score,
                                                'mode': lastGame.idMode.nom,
                                                'difficulte': lastGame.idMode.difficulte,
                                                'columnNamesHisto': columnNamesHisto,
                                                'partiesHisto': historiqueParties,
                                                'columnNamesClass': columnNamesClass,
                                                'partiesClass': classementParties})
    except:
        # section classement
        columnNamesClass = ['Joueur','Date', 'Durée', 'Nom du mode', 'Difficulte du mode','Score']
        classementParties = Request_BDD.getClassement()
        
        return render(request,"classement.html",{'nom':nom,
                                                'score': '/',
                                                'mode': '/',
                                                'difficulte': '/',
                                                'columnNamesHisto': [],
                                                'partiesHisto': [],
                                                'columnNamesClass': columnNamesClass,
                                                'partiesClass': classementParties})

def contact(request):
    nom = checkSession(request)
    return render(request,"contact.html",{'nom':nom})


def gamefinal(request):
    nom = checkSession(request)
    if nom != "":
        if request.method == "GET":
            
            modeSelected = request.GET.get('mode')
            difficulteSelected = request.GET.get('difficulte')

            print('Mode :', modeSelected , ' | Difficulte :', difficulteSelected)

            # AJOUTER verifification identité avec faceNet ...
            # Scripts python: appel faceNet en fonction du lien du modele
            # Stocker la vérification dans un cookie pour éviter l'identification à chaque game
            
            idPartie, temps = Request_BDD.addPartie(1, modeSelected, difficulteSelected, request.session['mail'])
            Request_BDD.modificationPartie(idPartie, 92, 300)

            print("Temps", temps)
            return render(request,"gamefinal.html",{'nom':nom, 'partie': idPartie, 'tempsImparti': temps})

    else : 
        return redirect('jouer')

def game2(request):
    nom = checkSession(request)

    if nom != "":
        if request.method == "GET":
            
            modeSelected = request.GET.get('mode')
            difficulteSelected = request.GET.get('difficulte')

            print('Mode :', modeSelected , ' | Difficulte :', difficulteSelected)

            # AJOUTER verifification identité avec faceNet ...
            # Scripts python: appel faceNet en fonction du lien du modele
            # Stocker la vérification dans un cookie pour éviter l'identification à chaque game
            
            #idPartie, temps = Request_BDD.addPartie(2, modeSelected, difficulteSelected, request.session['mail'])
            #Request_BDD.modificationPartie(idPartie, 92, 300)

            #print("Temps", temps)
            return render(request,"game2.html")

    else : 
        return redirect('jouer')

def game1(request):
    return render(request,"game.html")




def mode_perso(request):
    print("ok")
    nom = checkSession(request)
    form = forms.mode_perso_form()
    print("51515")
    if request.method == "POST":
        print("1818")
        form = forms.mode_perso_form(request.POST)
        if form.is_valid():
            infos = request.POST
            print(infos)
            Request_BDD.addMode(infos["nom"], infos['difficulte'], infos['tempsImparti_mode'], infos['pointsNegatifsOn_mode'])
            return redirect('jouer')
        else:
            return render(request,"mode_perso.html", {'form' : form, 'nom':nom})
        
    else:
        print("fefe")
        return render(request,"mode_perso.html", {'form' : form, 'nom':nom})



def authentification(request):
    nom = checkSession(request)
    if nom != "":
        if request.method == "GET":
            
            modeSelected = request.GET.get('mode')
            difficulteSelected = request.GET.get('difficulte')
            print('Mode :', modeSelected , ' | Difficulte :', difficulteSelected)
            
            if verifyAuth(request):
                return redirect("game2")

            # AJOUTER verifification identité avec faceNet ...
            # Scripts python: appel faceNet en fonction du lien du modele
            # Stocker la vérification dans un cookie pour éviter l'identification à chaque game
            
            #idPartie, temps = Request_BDD.addPartie(2, modeSelected, difficulteSelected, request.session['mail'])
            #Request_BDD.modificationPartie(idPartie, 92, 300)

            #print("Temps", temps)
            return render(request,'authentification.html',{'mode':modeSelected,'difficulte':difficulteSelected,'nom':nom})

    else : 
        return redirect('jouer')
   