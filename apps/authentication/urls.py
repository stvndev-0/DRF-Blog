from django.urls import path
from .views import (
    ResetPasswordView,
    SendResetEmailView,
    ActivationEmailView,
    SignUpView)

urlpatterns = [
    path('reset-password/<str:uidb64>/<str:token>', ResetPasswordView.as_view(), name='password-reset-confirm'),
    path('send-reset-email', SendResetEmailView.as_view()),
    path('activation-email/<str:uidb64>/<str:token>', ActivationEmailView.as_view(), name='activation-email'),
    path('signup', SignUpView.as_view())
]