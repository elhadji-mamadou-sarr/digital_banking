from django.shortcuts import render
from .models import BankAccount
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializer import BankAccountSerializer, UserSerializer
from rest_framework import status 
from django.contrib.auth.models import User
from .filters import BankAccountFilter
from rest_framework.filters import OrderingFilter
import django_filters


class ListAccountView(generics.ListAPIView):
  queryset = BankAccount.objects.all()
  serializer_class = BankAccountSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = BankAccountFilter
  ordering_fields = ['numero_compte'] 

class DetailApiView(generics.RetrieveAPIView):
  queryset = BankAccount.objects.all()
  serializer_class = BankAccountSerializer
  
  

class CreateApiView(generics.CreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        bank_account = BankAccount.objects.create(**validated_data)
        
        #Activer l'utilisateur associé au compte bancaire
        user = validated_data.get('client')
        if user and not user.is_active:
            user.is_active = True
            user.save()

        return bank_account
   
   
class UpdateApiView(generics.UpdateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwarg = 'pk'  

    def perform_update(self, serializer):
        numero_compte = serializer.validated_data.get('numero_compte')
        client = serializer.validated_data.get('client')
        solde = serializer.validated_data.get('solde')
        serializer.save()
     

class DeleteApiView(generics.DestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    lookup_url_kwarg = 'pk'  

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


