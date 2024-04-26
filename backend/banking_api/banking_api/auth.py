from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status 
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from banking.serializer import UserLoginSerializer, UserSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
      return Response({"detai" : "Not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserLoginSerializer(instance=user)
    return Response({"oken": token.key, "user" : serializer.data})

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
 