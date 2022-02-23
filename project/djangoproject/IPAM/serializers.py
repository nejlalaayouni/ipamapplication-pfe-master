from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vlan
from .models import Sousreseau
from .models import Adresseip
from .models import Hote

User = get_user_model()

class vlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vlan
    fields='__all__'
    
class sousreseauSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sousreseau
    fields='__all__'
 
class adresseipSerializer(serializers.ModelSerializer):
  class Meta:
    model = Adresseip
    fields='__all__' 

class userSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields='__all__'

class hoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hote
    fields='__all__'
