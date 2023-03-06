from . import views
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,TokenVerifyView ,TokenObtainPairView)
#  http://127.0.0.1:8000/users/index
urlpatterns = [
    path('api/', views.TestAPIView.as_view()),
    path('sign_up/', views.create_user),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('verify/token/', TokenVerifyView.as_view(), name='token_verify_api'),

]
