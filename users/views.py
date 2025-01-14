import random
import uuid

from django.db import IntegrityError
from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Device

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer



class RegisterView(APIView):
    
    def post(self, request):
        # Get phone number from request
        phone_number = request.data.get('phone_number')
        
        # Input validation
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(phone_number, str):
            return Response ({'error':'Invalid phone number format'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user, is_new_user = User.objects.get_or_create(
                phone_number=phone_number, password = make_password(phone_number),# Hash the password
                defaults={'username': get_random_string(length=10)}) # Random unique username
        except IntegrityError:
            return Response({'error':'Phone number already registered'}, status=status.HTTP_409_CONFLICT)
            
            # # If user already exists
            # if not is_new_user:
            #     return Response(
            #         {'detail': 'user already registered!'},
            #         status=status.HTTP_409_CONFLICT)
            
        # Generate verification code
        verification_code = random.randint(10000, 99999)
        
        # caching----(myKey, myValue, timestamp)
        cache.set(str(verification_code), str(verification_code), timeout=300)
        
        # Simulate sending the verification code (replace with SMS logic)
        print (f"Verification code sent: {verification_code}")
        
        return Response ({"message": "Verification code sent"}, status=status.HTTP_200_OK)
    
    
    
class VerifyCodeView(APIView):
    
    def post(self, request):
        verification_code = request.data.get('verification_code')
        
        if not verification_code:
            return Response ({"Error":"Verification code required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        stored_cache = cache.get(verification_code)
        
        if stored_cache != verification_code:
            raise AuthenticationFailed("Invalid or expired verification code")
        
        cache.delete(verification_code)
        
        user = User.objects.create()
        
        return Response({'message':'Verification code verified successfully'}, status=status.HTTP_200_OK)
        
        
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
            
        

# Because now we have a jwt auth
# class GetTokenView(APIView):
    
#     # Get phone and code from request
#     def post(self, request):
#         phone_number = request.data.get('phone_number')
#         user_code = request.data.get('code')
        
#         # Get saved code from cache
#         saved_code = cache.get(str(phone_number))
        
#         # Check if the codes match
#         if user_code!= saved_code:
#             return Response({'Error': 'The provided code is wrong!'}, status=status.HTTP_401_UNAUTHORIZED)
        
#         # Generate new token
#         token = str(uuid.uuid4())
        
#         return Response({'token': token})