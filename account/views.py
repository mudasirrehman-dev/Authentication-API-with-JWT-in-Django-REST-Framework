from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializer import UserRegistrationSerializer,UserLoginSerializer,UserPasswordResetSerializer,UserProfileSerializer,SendPasswordResetEmailSerializer,UserChangePasswordSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated



# Create your views here.

#Creating tokens manually
def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request , format=None):
        serializer= UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'Register Token': token ,'msg':'Registration sucssfull.'}, status=status.HTTP_201_CREATED)     
        return Response(serializer.errors,{'msg':'Registration Failed.'} , status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user =authenticate(email=email , password=password)
            print(user, email, password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'Login Token':token,'msg':'User Found and login Succssful.'}, status=status.HTTP_200_OK)
            return Response({'errors':{'non_field_errors':['Email and Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    
    def get(self, request , format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    
    def post(self, request , format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderers]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Please Check your Email! & Re-Set Your Password.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    
    def post(self, request, userId, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data ,context={'userId': userId , 'token': token} )
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Re-Set Successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)                