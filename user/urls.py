from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/',UserProfileView.as_view()),
    
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Get access & refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh access token
]