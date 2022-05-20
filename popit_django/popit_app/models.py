from django.db import models
from datetime import date

# Create your models here.

#class Jeu(models.Model):
    #idJeu = models.AutoField(primary_key=True)

class Mode(models.Model):
    idMode = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    difficulte = models.CharField(max_length=255)
    tempsImparti = models.IntegerField(default=0)
    pointsNegatifsOn = models.BooleanField(default=False)

"""
class Classement(models.Model):
    idClassement = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    idJeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
"""

class Modele(models.Model):
    idModele = models.AutoField(primary_key=True)  
    lien_pkl = models.CharField(max_length=255,default="")
    lien_pb = models.CharField(max_length=255,default="")


class Joueur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=255,primary_key=True)
    pseudo = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)
    #idJeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)

class Partie(models.Model):
    idPartie = models.AutoField(primary_key=True)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    duree = models.DurationField(default="00:00:00") 
    idModele = models.ForeignKey(Modele, on_delete=models.CASCADE)
    idMode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    idJoueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
    #idJeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)


