from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from .serializers import LoginSerializer

class LoginUser(APIView):
    @swagger_auto_schema(
            request_body=LoginSerializer,
            operation_summary='Вход пользователя',
    )
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']
                user = authenticate(username=username,
                                    password=password)
                if user is None:
                    return Response({"response":"error"}, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = RefreshToken.for_user(user)
                return Response({"response":"success", 
                                 "user": {
                                     "access": str(refresh.access_token),
                                     'refresh': str(refresh),
                                 }})
            else:
                return Response({"response": "error"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"response":"error"}, status=status.HTTP_400_BAD_REQUEST)