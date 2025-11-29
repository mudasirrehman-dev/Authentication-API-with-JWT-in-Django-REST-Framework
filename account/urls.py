from django.urls import path 
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserPasswordResetView,SendPasswordResetEmailView,UserChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-mail-to-set-password/', SendPasswordResetEmailView.as_view(), name='send-mail-to-set-password'),
    path('reset-password/<userId>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
]