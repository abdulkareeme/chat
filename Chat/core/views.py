from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer , ListUserSerializer
from rest_framework.views import APIView
from .models import User
from django.db.models import Q
from rest_framework import status , permissions


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_info':{
            'id': user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
        },
        'token':{token}
    })

@api_view(['GET'])
def user_info(request):
    user = request.user
    if user.is_authenticated:
        return Response({
                'user_info':{
                'id': user.id,
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name
            },
        })



@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
                'user_info':{
                'id': user.id,
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name
            },
        })
    
class ListUser(APIView):
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self , request):
        users = User.objects.filter(~Q(pk=request.user.pk))
        serializer = ListUserSerializer(users , many=True)
        # print(serializer.validated_data)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status.HTTP_200_OK)
    