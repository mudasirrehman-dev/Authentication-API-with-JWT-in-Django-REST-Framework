from rest_framework import serializers
from account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} , write_only=True)
    tc = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password',  'password2', 'tc']
        
        extra_kwargs={
            'password':{'write_only': True}
        }
        
    #Now Validate the password and confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password did not match to confirm password!")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    # i comment it because it  does not return the password.
    #password = serializers.CharField(write_only=True)    
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'} , write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'} , write_only=True)
    
    class Meta:
        fields = ['password','password2']
        
    #Now Validate the password and confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password did not match to confirm password!")
        user.set_password(password)
        user.save()
        return attrs