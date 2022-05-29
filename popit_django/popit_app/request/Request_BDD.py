from ..models import *

import datetime as dt
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
    def inscription(mail_user, nom_user, prenom_user, password_user, pays_user, pseudo_user):
        if Joueur.objects.filter(email__exact = mail_user).count() == 0: #Vérification que l'adresse mail ne soit pas déjà utilisée
            ajoutJoueur = Joueur.objects.create(
                email = mail_user,
                password = make_password(password=password_user),
                prenom = prenom_user,
                pseudo = pseudo_user,
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
                    pointsNegatifsOn = pointsNegatifsOn_mode
                )
            return 'OK'
        else:
            if Mode.objects.filter(nom__exact=nom_mode, difficulte__exact=difficulte_mode).count()==0:
                ajoutMode = Mode.objects.create(
                    nom = nom_mode,
                    difficulte = difficulte_mode,
                    tempsImparti = tempsImparti_mode,
                    pointsNegatifsOn = pointsNegatifsOn_mode
                )
                return 'OK'
            else:
                return 'mode déjà présent'


    # Ajout Modele
    def addModele(lien_pkl,lien_pb):
        if (Modele.objects.filter(lien_pkl__exact=lien_pkl,lien_pb__exact=lien_pb).count()==0) :
            ajoutModele = Modele.objects.create(
                lien_pkl = lien_pkl,
                lien_pb = lien_pb
            )
            return 'OK'
        else:
            return 'modele déjà présent'


    # Ajout Partie
    def addPartie(modele_partie, nom_mode, difficulte_mode, joueur):
        # A compléter pour récupérer les informations correspondantes !!!!!!!!
        modele = Modele.objects.get(pk= modele_partie) # A récupérer de l'organisation du joueur
        mode = Mode.objects.get(nom__exact=nom_mode, difficulte__exact = difficulte_mode) # A Tester
        joueur = Joueur.objects.get(pk = joueur)

        newPartie = Partie.objects.create(
            score= 0,
            date = datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            duree =  dt.timedelta(days=0, hours=0, minutes=0, seconds =0), # A initialiser à 0
            idModele = modele,
            idMode = mode,
            idJoueur = joueur
        )
        return newPartie.pk, mode.tempsImparti


    ############### SUPPRESSION D'ELEMENTS ###############
    def viderTable():
        Partie.objects.all().delete()
        Joueur.objects.all().delete()
        #Mode.objects.all().delete()
        #Modele.objects.all().delete()

    def afficherTable():
        print(Partie.objects.all())
        print(Joueur.objects.all())
        print(Mode.objects.all())
        print(Modele.objects.all())


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
        supp = Partie.objects.get(pk = idPartie)
        supp.delete()


    ############### MODIFICATION D'ELEMENTS ###############
    def modificationJoueur(email, nom, prenom, password, pays, pseudo):
        # Impossible de modifier l'email (pour l'instant)
        modifJoueur = Joueur.objects.get(email__exact = email)
        modifJoueur.nom = nom
        modifJoueur.prenom = prenom
        modifJoueur.pseudo = pseudo
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

        modifPartie = Partie.objects.get(pk = idPartie)
        modifPartie.score = score
        modifPartie.duree = dt.timedelta(days=0, hours=0, minutes=0, seconds=duree)
        modifPartie.save()

    # Pas de modification de mode possible -> obligation de suppresion et puis création

    ############### OBTENTION D'INFORMATIONS ###############
    def getNomJoueur(email):
        joueur = Joueur.objects.get(email__exact = email)

        return joueur.prenom

    def verifyDisponiblePseudo(pseudo_user):
        return Joueur.objects.filter(pseudo__exact = pseudo_user).count()


    # récupérer les infos de la denière partie du joueur connecté
    def getLastGame(email):
        PartiesSorted = Partie.objects.filter(idJoueur__exact = email).order_by("-date")

        return PartiesSorted[0]


    # Modifier la récupération du joueur concerné idJoueur -> email ?
    def getHistoriquePerso(joueur):
        infosParties= []
        try:
            infos = list(Partie.objects.filter(idJoueur__exact = joueur).values_list('date','duree','score','idMode'))
            for elem in infos:
                infosMode = Mode.objects.get(pk = elem[3])
                infosPartie = list(elem)[:-2] + [infosMode.nom, infosMode.difficulte, list(elem)[2]]
                infosParties.append(infosPartie)
            return infosParties

        except:
            return infosParties
        

    def getClassement():
        infosParties = []

        try:
            infos = list(Partie.objects.all().values_list('idJoueur','date','duree','score','idMode'))
            for elem in infos:
                infosMode = Mode.objects.get(pk = elem[4])
                pseudoJoueur = Joueur.objects.get(email__exact = list(elem)[0]).pseudo
                infosPartie = [pseudoJoueur,list(elem)[1],list(elem)[2]] + [infosMode.nom, infosMode.difficulte, list(elem)[3]]
                infosParties.append(infosPartie)
            return infosParties

        except:
            return infosParties


    def getMode():
        modesDisponibles = []
        modes =  Mode.objects.values('nom').distinct()
        for mode in modes:
            modesDisponibles.append(mode['nom'])

        return modesDisponibles


    def getDifficultes(modeNom):
        difficulte = list(Mode.objects.filter(nom__exact = modeNom).values('difficulte'))

        return difficulte



