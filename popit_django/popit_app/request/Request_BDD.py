from django.forms import modelformset_factory
from ..models import *

from datetime import datetime, date, timedelta
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password


class Request_BDD():
    ############### CONNEXION ###############
    def connexion(mail_user, password_user):
        mail = mail_user
        password = password_user

        verification = False

        # On regarde s'il y a bien quelqu'un avec cet email dans la base de données
        verifUser = Joueur.objects.filter(email__exact = mail).count()
        if verifUser == 0:
            verification = False

        else:
            verifUser = Joueur.objects.filter(email__exact = mail).values_list('email','password','nom','prenom')
            verifUser=list(*list(verifUser))
            comparaison=check_password(password, verifUser[1])
            if comparaison==True:
                verification=True

        return verification

    ############### AJOUT D'ELEMENTS ###############

    # Inscription (ajout d'un nouveau joueur)
    def inscription(mail_user, nom_user, prenom_user, password_user, pays_user):
        if Joueur.objects.filter(email__exact = mail_user).count() == 0: #Vérification que l'adresse mail ne soit pas déjà utilisée
            ajoutJoueur = Joueur.objects.create(
                email = mail_user,
                password = make_password(password=password_user),
                prenom = prenom_user,
                nom = nom_user,
                pays = pays_user
            )
            return 'OK'
        else:
            return 'NOK'


    # Ajout d'un nouveau mode
    def addMode(nom_mode, difficulte_mode, tempsImparti_mode, pointsNegatifsOn_mode):
        # Verification que ce mode n'existe pas
        if Mode.objects.filter(nom__exact=nom_mode).count()==0:
            ajoutMode = Mode.objects.create(
                    nom = nom_mode,
                    difficulte = difficulte_mode,
                    tempsImparti = tempsImparti_mode,
                    PointsNegatifsOn = pointsNegatifsOn_mode
                )
            return 'OK'
        else:
            if Mode.objects.filter(difficulte__exact=difficulte_mode).count()==0:
                ajoutMode = Mode.objects.create(
                    nom = nom_mode,
                    difficulte = difficulte_mode,
                    tempsImparti = tempsImparti_mode,
                    PointsNegatifsOn = pointsNegatifsOn_mode
                )
                return 'OK'
            else:
                return 'mode déjà présent'


    # Ajout Modele
    def addModele(lien_modele):
        if (Mode.objects.filter(lien__exact=lien_modele).count()==0):
            ajoutModele = Modele.objects.create(
                lien = lien_modele
            )
            return 'OK'
        else:
            return 'modele déjà présent'


    # Ajout Partie
    def addPartie(modele_partie, mode_partie, joueur):
        # A compléter pour récupérer les informations correspondantes !!!!!!!!
        modele = "" # A récupérer de l'organisation du joueur
        mode = "" # A récupérer de la saisie de l'utilisateur
        joueur = "" # A récupérer du profil de l'utilisateur

        # AJOUTER verifification identité avec faceNet ...
        # Scripts python: appel faceNet en fonction du lien du modele

        ajoutPartie = Partie.objects.create(
            score= 0,
            date = datetime.today().strftime('%Y-%m-%d'),
            duree = 0,
            idModele = modele,
            idMode = mode,
            idJoueur = joueur
        )


    ############### SUPPRESSION D'ELEMENTS ###############
    def suppressionJoueur(email):
        supp = Joueur.objects.get(email__exact = email)
        supp.delete()

    def suppressionMode(nom, difficulte):
        supp =  Mode.objects.filter(nom__exact=nom, difficulte__exact = difficulte)
        supp.delete()

    def suppresionModele(lien):
        supp = Modele.objects.filter(lien__exact = lien)
        supp.delete()

    def suppressionpartie(idPartie):
        supp = Partie.objects.filter(idPartie__exact = idPartie)
        supp.delete()


    ############### MODIFICATION D'ELEMENTS ###############
    def modificationJoueur(email, nom, prenom, password, pays):
        # Impossible de modifier l'email (pour l'instant)
        modifJoueur = Joueur.objects.get(email__exact = email)
        modifJoueur.nom = nom
        modifJoueur.prenom = prenom
        modifJoueur.password = password
        modifJoueur.pays = pays
        modifJoueur.save()

    def modificationModele(lien, nouveauLien):
        modifModele = Modele.objects.get(lien__exact = lien)
        modifModele.lien = nouveauLien
        modifModele.save()

    def modificationPartie(idPartie, score, duree):
        # Score à récupérer de l'interface
        # Durée, à récupérer également de l'interface

        modifPartie = Partie.objects.get(idPartie__exact = idPartie)
        modifPartie.score = score
        modifPartie.duree = duree 
        modifPartie.save()

    # Pas de modification de mode possible -> obligation de suppresion et puis création

    ############### OBTENTION D'INFORMATIONS ###############
    def getNomJoueur(email):
        joueur = Joueur.objects.filter(email__exact = email).values_list('nom')
        joueur = list(*list(joueur))

        return joueur[0]

    # Modifier la récupération du joueur concerné idJoueur -> email ?
    def getHistoriquePerso(joueur):
        # joueur = idJoueur
        infosParties = []
        infos = Partie.objects.filter(email__exact = joueur).values_list('idPartie','score','date','duree', 'idMode')
        infos=list(*list(infos))
        
        infosMode = Mode.objects.filter(idMode__exact = infos[4]).values_list('nom','difficulte')
        infosMode=list(*list(infosMode))

        infosGlobales = infos.append(*list(infosMode))

        return infosGlobales
        # Sorties à tester !!

        return infosParties

    def getClassementOneFilter(filter):
        # TO DO
        return "None"

