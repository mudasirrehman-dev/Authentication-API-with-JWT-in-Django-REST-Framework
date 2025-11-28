from django.urls import path 
from account.views import UserRegistrationView,UserLoginView,UserProfileView,SendPasswordResetEmailView,UserChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('Re-set-password/', SendPasswordResetEmailView.as_view(), name='Re-set-password'),
]