from django.urls import path

# Authentication URLS
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView, VerifyCodeView

urlpatterns = [
  path('register/', RegisterView.as_view()),
  path('verify/', VerifyCodeView.as_view()),
  # Because now we have a jwt auth
  # path('get-token/', GetTokenView.as_view()),
  
  path('users/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]