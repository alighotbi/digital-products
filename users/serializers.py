from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'phone_number'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'] = serializers.CharField()
        del self.fields['password']

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        
        if not phone_number:
            raise AuthenticationFailed('Phone number is required.')
        
        # Validate the user
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise AuthenticationFailed('User with this phone number does not exist.')

        # Generate tokens for the user
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            
            # Response with User Details
            'user':{
                'id': user.id,
                'phone_number': user.phone_number,
            }
        }
