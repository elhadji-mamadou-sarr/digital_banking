from django.shortcuts import render
#from .models import BankAccount
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from banking.serializer import UserSerializer
from rest_framework import status 
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication



# Create your views here.

@authentication_classes([TokenAuthentication])
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@authentication_classes([TokenAuthentication])
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
   

@authentication_classes([TokenAuthentication])
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

    serialized_users = [{'id': user.id, 'username': user.first_name, 'username': user.last_name, 'email': user.email} for user in inactive_users]

    return Response(serialized_users, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = request.data.get('token')
            token_obj = Token.objects.get(key=token)
            token_obj.delete()
            return Response({'success': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
