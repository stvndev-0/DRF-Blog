from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    SetNewPasswordSerializer,
    SignUpSerializer
)
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .utils import generate_token
from .tasks import reset_password, verify_account

User = get_user_model()

class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(
            data=request.data,
            context={
                'uidb64': uidb64,
                'token': token
            }
        )
        
        if serializer.is_valid():
            return Response({
                'detail': 'Your new password has been set.'
                }, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class SendResetEmailView(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.get(email=email)

        try:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            
            reset_password.delay(uidb64, token ,email)

            return Response({
                'detail': 'Code send to email.'
                }, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response({
                'detail': 'Email does not exist.'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class ActivationEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decodifica el parametro uidb64 y lo pasa a cadena (str)
            uidb = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uidb)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({
                'detail': 'Invalid user or corrupt token.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        if not generate_token.check_token(user, token):
            return Response({
                'detail': 'Invalid token or expired.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        user.verified = True
        user.save()
        
        return Response({
            'detail': 'Email verified successfully.'
            }, status=status.HTTP_200_OK
        )

class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Codifica el pk del usuario a bytes para generar una url encriptada, y genera un token unico para el usuario
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)

            # tasks
            verify_account.delay(uidb64, token, email=user.email)

            return Response({
                'detail': 'Verify your email address.',
                }, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    