from . import views
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView, TokenObtainPairView)
#  http://127.0.0.1:8000/users/index
urlpatterns = [
    path('sign_up/', views.create_user),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('verify/token/', TokenVerifyView.as_view(), name='token_verify_api'),
    path('login/', TokenObtainPairView.as_view(), name='login_api'),
    path('list/', views.user_list, name='user_list_api'),
    path('<int:pk>', views.get_user, name='get_user_api'),
    path('update_user_profile/', views.update_user, name='update_user_profile_api'),
    path('edge/', views.UserNetworkEdgeView.as_view(), name='edge_api')
]
