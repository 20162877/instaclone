from . import views
from django.urls import path
#  http://127.0.0.1:8000/users/index
urlpatterns = [
    path('api/', views.TestAPIView.as_view()),
    path('sign_up/', views.create_user)
]
