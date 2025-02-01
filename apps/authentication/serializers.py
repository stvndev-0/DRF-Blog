from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utils import generate_token

User = get_user_model()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        try:
            uidb = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk=uidb)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({'detail': 'Invalid user or corrupt token.'})

        if not generate_token.check_token(user, token):
            raise serializers.ValidationError({'detail': 'Invalid token or expired.'})
        
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({'detail': "Password don't match."})
        
        validate_password(data['new_password'], user=user)

        user.set_password(data['new_password'])
        user.save()

        return data

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def validate_email(self, value):
        email = value.endswith('@gmail.com')
        if not email:
            raise serializers.ValidationError({'detail': 'Only emails under the gmail domain are allowed.'})
        return value
    
    def create(self, validated_data):
        email = self.validate_email(validated_data['email'])
        username = validated_data['email']
        user= User.objects.create_user(
            username=username.split('@')[0],
            email=email,
            password=validated_data['password']
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email, verified=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail':'Incorrect username or password.'})
        
        if not check_password(password, user.password):
            raise serializers.ValidationError({'detail': 'Incorrect username or password.'})
        
        return data