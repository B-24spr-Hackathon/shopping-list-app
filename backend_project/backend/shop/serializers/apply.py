from rest_framework import serializers
from shop.models import  User, List

   
class OwnListsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = List
        fields = ('list_id', 'list_name')