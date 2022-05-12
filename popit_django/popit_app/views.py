from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
import cv2
import numpy as np

from . import forms
from django.contrib.auth import login
from .request.Request_BDD import Request_BDD


# FONCTIONS POUR LE JEU 

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        ret, frame = self.cap.read()
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)
        return frame.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
    video_object=gen(VideoCamera())
    return StreamingHttpResponse(video_object,content_type='multipart/x-mixed-replace; boundary=frame')


def game(request):
    return render(request,"game.html")



#CHECK SESSION
def checkSession(request):
    try:
        nom = request.session['nom']
    except:
        nom = ""
    return nom


# ARCHITECTURE APPLICATION    

def accueil(request):
    nom = checkSession(request)
    return render(request,"accueil.html",{'nom':nom})

def inscription(request):
    nom = checkSession(request)
    form =  forms.inscription_form()
    if request.method == "POST":
        form = forms.inscription_form(request.POST)
        
        if form.is_valid():
            infos = request.POST
            if infos['password'] == infos['password2']:
                Request_BDD.inscription(infos['email'], infos['nom'], infos['prenom'], infos['password'], infos['pays'])
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
    return render(request,"accueil.html",{'nom':nom})

def jouer(request):
    nom = checkSession(request)
    #Request_BDD.addPartie(1, 1, request.session['mail'])
    #Request_BDD.modificationPartie(1, 50, 180)
    return render(request,"jouer.html",{'nom':nom})

def classement(request):
    nom = checkSession(request)
    try:
        lastGame = Request_BDD.getLastGame(request.session['mail'])
    
        return render(request,"classement.html",{'nom':nom, 'score': lastGame.score, 'mode': lastGame.idMode.nom, 'difficulte': lastGame.idMode.difficulte})
    except:
        return render(request,"classement.html",{'nom':nom, 'score': '/', 'mode': '/', 'difficulte': '/'})

def contact(request):
    nom = checkSession(request)
    return render(request,"contact.html",{'nom':nom})

def game2(request):
    nom = checkSession(request)
    return render(request,"game2.html",{'nom':nom})

def game1(request):
    return render(request,"game.html")







