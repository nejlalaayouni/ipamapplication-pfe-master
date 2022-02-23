from django.db import models

# Create your models here.

class Vlan(models.Model):
    idvlan = models.CharField(max_length=15)
    nom = models.CharField(max_length=20, unique=True)
    description = models.TextField()

class History_vlan(models.Model):
    date_action = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)
    ancien_nom = models.CharField(max_length=20, default=' ')
    nouveau_nom = models.CharField(max_length=20, default=' ')
    ancien_idvlan = models.CharField(max_length=15, default=' ')
    nouveau_idvlan = models.CharField(max_length=15, default=' ')


class Sousreseau(models.Model):
    nom = models.CharField(max_length=20)
    adresse = models.CharField(max_length=20, unique=True)
    taille = models.IntegerField()
    vlan = models.ForeignKey(Vlan, on_delete=models.CASCADE, null=True)
    etat = models.BooleanField(default=False)
    derniere_scan = models.DateTimeField(null=True)

class History_sousreseau(models.Model):
    date_action = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)
    nouveau_nom = models.CharField(max_length=20, default=' ')
    nouveau_adresse= models.CharField(max_length=20, default=' ')
    ancien_nom = models.CharField(max_length=20, default=' ')
    ancien_adresse= models.CharField(max_length=20, default=' ')
    date_scan = models.CharField(max_length=50, default=' ')

class Hote(models.Model):
    nom = models.CharField(max_length=20)
    sousreseau = models.ForeignKey(Sousreseau, on_delete=models.CASCADE, null=True)
    etat = models.BooleanField(default=False)

    
class Adresseip(models.Model):
    nom = models.CharField(max_length=20)
    adresse = models.CharField(max_length=20)
    sousreseau = models.ForeignKey(Sousreseau, on_delete=models.CASCADE, null=True)
    etat = models.BooleanField(default=False)
    utliser = models.BooleanField(default=False)
    disponible = models.BooleanField(default=False)


class History_adresseip(models.Model):
    date_action = models.DateTimeField(auto_now_add=True)
    nouveau_nom = models.CharField(max_length=20, default=' ')
    nouveau_adresse= models.CharField(max_length=20, default=' ')
    etat = models.BooleanField(default=False)
   

class Tacheanalyse(models.Model):
    nom = models.CharField(max_length=20)
    temp = models.CharField(max_length=20)
    date_tache = models.DateField()
    etat = models.BooleanField(default=False)
    date_creation = models.DateTimeField(null=True)
    sousreseau = models.ForeignKey(Sousreseau, on_delete=models.CASCADE, null=True)


class History_tacheanalyse(models.Model):
    date_action = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)
    nouveau_nom = models.CharField(max_length=20, default=' ')
    nouveau_adresse= models.CharField(max_length=10, default=' ')
    ancien_nom = models.CharField(max_length=20, default=' ')
    ancien_adresse= models.CharField(max_length=10, default=' ')
    
    




