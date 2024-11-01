from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import CRMUserViewSet, CustomTokenObtainPairView

users_router = DefaultRouter()
users_router.register(prefix='', viewset=CRMUserViewSet, basename='users')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(users_router.urls)),
]
