from django.shortcuts import render
#from .models import BankAccount
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from banking.serializer import UserSerializer
from rest_framework import status 
from django.contrib.auth.models import User

# Create your views here.

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
   


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'pk' 
    
    
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'pk'
    
    
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'pk' 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def inactive_users_view(request):
    
    inactive_users = User.objects.filter(is_active=False)

    # Serializer la liste des utilisateurs inactifs
    serialized_users = [{'id': user.id, 'username': user.first_name, 'username': user.last_name, 'email': user.email} for user in inactive_users]

    return Response(serialized_users, status=status.HTTP_200_OK)