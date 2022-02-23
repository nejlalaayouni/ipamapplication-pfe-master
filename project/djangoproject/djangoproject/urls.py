"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from IPAM import views
from IPAM import cron
from IPAM import api
from django.conf import settings
from django.urls import reverse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', views.demo, name="demo"),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('vlan/', views.vlan, name="vlan"),
    path('vlan/ajoutervlan/', views.ajoutervlan, name="ajoutervlan"),
    path('vlan/modifvlan/<int:id>', views.modifvlan, name="modifvlan"),
    path('vlan/suppvlan/<int:id>', views.suppvlan, name="suppvlan"),
    path('historyvlan/', views.historyvlan, name="historyvlan"),
    path('historyvlan/supphistovlan', views.supphistovlan, name="supphistovlan"),
    path('sousreseau/', views.sousreseau, name="sousreseau"),
    path('sousreseau/ajoutsousreseau/', views.ajoutsousreseau, name="ajoutsousreseau"),
    path('sousreseau/suppsousreseau/<int:id>', views.suppsousreseau, name="suppsousreseau"),
    path('sousreseau/detailsousreseau/<int:id>', views.detailsousreseau, name="detailsousreseau"),
    path('sousreseau/ipsousreseau/<int:id>', views.ipsousreseau, name="ipsousreseau"),
    path('historysousreseau/', views.historysousreseau, name="historysousreseau"),
    path('historysousreseau/supphistosousreseau', views.supphistosousreseau, name="supphistosousreseau"),
    path('ipadresses/<int:id>', views.ipadresses, name="ipadresses"),
    path('attadressesip/<int:id>', views.attadressesip, name="attadressesip"),
    path('ipadresses/attribipadresses/<int:id>', views.attribipadresses, name="attribipadresses"),
    path('ipadresses/anulattribipadresses/<int:id>/<str:hote>', views.anulattribipadresses, name="anulattribipadresses"),
    path('historyadresseip/', views.historyadresseip, name="historyadresseip"),
    path('historyadresseip/supphistoadresseip', views.supphistoadresseip, name="supphistoadresseip"),
    path('tacheanalyse/', views.tacheanalyse, name="tacheanalyse"),
    path('tacheanalyse/creetacheanalyse/', views.creetacheanalyse, name="creetacheanalyse"),
    path('tacheanalyse/modiftacheanalyse/<int:id>', views.modiftacheanalyse, name="modiftacheanalyse"),
    path('tacheanalyse/supptacheanalyse/<int:id>', views.supptacheanalyse, name="supptacheanalyse"),
    path('historytacheanalyse/', views.historytacheanalyse, name="historytacheanalyse"),
    path('historytacheanalyse/supphistotacheanalyse', views.supphistotacheanalyse, name="supphistotacheanalyse"),
    path('ipadresses/scan/<int:id>', views.scan, name="scan"),
    path('rapport/', views.rapport, name="rapport"),
    #############################
    #path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('rest_auth.urls')),
    path('api/auth/', api.ShowProfile.as_view()), 
    ##VLAN####################
    path('api/vlan',api.vlanlistapi,name="vlanlistapi"),
    path('api/countvlan',api.countvlan,name="countvlan"),
    path('api/vlandetail/<int:id>',api.vlandetail,name="vlandetail"),
    ##Sous-réseaux############
    path('api/sousreseaux',api.sousreseaulistapi,name=" sousreseaulistapi"),
    path('api/countsousreseaux',api.countsousreseau,name=" countsousreseaux"),
    ##Adresse IP##############
    path('api/adresseip/<int:ids>',api.adresseiplistapi,name="adresseiplistapi"),
    path('api/countadresseip/',api.countadresseip,name="countadresseip"),
    path('api/adressipdetail/<int:id>',api.adressipdetail,name="adressipdetail"),
    path('api/adressipupdate/<int:ids>/<int:id>',api.adressipupdate,name="adressipupdate"),
    path('api/adresseipActive/',api.adresseipActive,name="adresseipActive"),
    ##Hote#####################
    path('api/hotelistapi/<int:idsr>',api.hotelistapi,name="hotelistapi"),
    path('api/attribadressip/<int:id>/<str:hote>/<int:idsr>',api.attribadressip,name="attribadressip"),
    path('api/anulattribadressip/<int:id>/<str:hote>/<int:idsr>',api.anulattribadressip,name="anulattribadressip"),
    path('api/adressiphote/<str:hotee>',api.adressiphote,name="adressiphote"),
    ############################
    path('ipadresses/cron_job/<int:id>',cron.cron_job,name="cron_job")
]
