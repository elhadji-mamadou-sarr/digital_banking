from rest_framework import serializers
from .models import BankAccount
from django.contrib.auth.models import User

class BankAccountSerializer(serializers.ModelSerializer):
    my_balance = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = BankAccount
        fields = ('numero_compte', 'client', 'solde', 'my_balance')
        
    def get_my_balance(self, obj):
        
        if not hasattr(obj, 'id'):
          return None
        if not isinstance(obj, BankAccount):
          return None
      
        return obj.get_balance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user