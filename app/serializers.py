from rest_framework import serializers
from .models import admin_table , katha_table , payment_table

class admin_serializer(serializers.ModelSerializer):
    class Meta:
        model = admin_table
        fields = '__all__'
class katha_serializer(serializers.ModelSerializer):
    class Meta:
        model = katha_table
        fields = '__all__'
class payment_serializer(serializers.ModelSerializer):
    class Meta:
        model = payment_table
        fields = '__all__'