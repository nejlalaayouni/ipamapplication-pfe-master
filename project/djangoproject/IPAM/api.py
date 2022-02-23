from rest_framework import status
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
#from rest_framework.test import APITestCase
from .models import Vlan
from .serializers import vlanSerializer
from .models import Sousreseau
from .serializers import sousreseauSerializer
from .models import Adresseip
from .serializers import adresseipSerializer
from .models import Hote
from .serializers import hoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .serializers import userSerializer
from rest_framework import generics
from django.db.models import Count
#from django.http import Http404
#from django.http import Http400
#from django.core.exceptions import PermissionDenied
#from django.core.exceptions import ValidationError
#from rest_framework import viewsets, status, exceptions
#from django.conf.urls import (
 ## handler400, handler403, handler404, handler500)

#from api.views import error404

#handler404 = error404

from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication



class ShowProfile(APIView):
	authentication_classes = (TokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		serializer = userSerializer(request.user)
		return Response(serializer.data)

################## VLAN ########################
@api_view(['GET'])
def vlanlistapi(request):
   #pass
    vlans=Vlan.objects.all()
    data=vlanSerializer(vlans,many=True).data
    return Response(data)

@api_view(['GET'])
def countvlan(request):
   #pass
    vlans=Vlan.objects.all().count()
    data={'vlancount':vlans}
    return Response(data)

@api_view(['GET'])
def vlandetail(request, id):
    vlan=Vlan.objects.get(id=id)
    serializer=vlanSerializer(vlan,many=False)
    return Response(serializer.data)

################### Sous-réseaux ##########################
@api_view(['GET'])
def sousreseaulistapi(request):
   #pass
    sousreseaux=Sousreseau.objects.all().order_by('id')
    data=sousreseauSerializer(sousreseaux,many=True).data
    return Response(data)    

@api_view(['GET'])
def countsousreseau(request):
   #pass
    sousreseaux=Sousreseau.objects.all().count()
    data={'sousreseauxcount':sousreseaux}
    return Response(data) 

#################### Adresse IP ################################
@api_view(['GET'])
def adresseiplistapi(request, ids):
   #pass
    ipadress=Adresseip.objects.filter(sousreseau_id=ids).all().order_by('id')
    data=adresseipSerializer(ipadress,many=True).data
    return Response(data) 

@api_view(['GET'])
def countadresseip(request):
   #pass
    ipadress=Adresseip.objects.filter().all().count()
    data={'adresseipcount':ipadress}
    return Response(data) 

@api_view(['GET'])
def adressipdetail(request, id):
    adressip=Adresseip.objects.get(id=id)
    serializer=adresseipSerializer(adressip,many=False)
    return Response(serializer.data)


@api_view(['POST'])
def adressipupdate(request, ids, id):
    adress=Adresseip.objects.get(sousreseau_id=ids, id=id)
    serializer=adresseipSerializer(instance=adress, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def adresseipActive(request):
   #pass
    ipadress=Adresseip.objects.filter(etat=1).all().order_by('id')
    data=adresseipSerializer(ipadress,many=True).data
    return Response(data) 

@api_view(['GET'])
def hotelistapi(request, idsr):  
    hote=Hote.objects.filter(sousreseau_id=idsr,etat=False).all()
    data=hoteSerializer(hote,many=True).data
    return Response(data) 


@api_view(['GET'])
def attribadressip(request, id, idsr, hote):
    adress=Adresseip.objects.filter(id=id).update(nom=hote,etat=True,utliser=True,disponible=True)
    hot=Hote.objects.filter(nom=hote, sousreseau_id=idsr).update(etat=True)
    serializer=adresseipSerializer(adress, many=False)
    serializer2=hoteSerializer(hot, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def anulattribadressip(request, id, idsr, hote):
    adress=Adresseip.objects.filter(id=id).update(nom="",etat=False,utliser=False,disponible=False)
    hot=Hote.objects.filter(nom=hote, sousreseau_id=idsr).update(etat=False)
    serializer=adresseipSerializer(adress, many=False)
    serializer2=hoteSerializer(hot, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def adressiphote(request, hotee):
    adressip=Adresseip.objects.filter(nom=hotee).all()
    data=adresseipSerializer(adressip,many=True).data
    return Response(data) 