from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import CRMUser, User
from apps.users.permissions import IsAdmin
from apps.users.serializers import CRMUserSerializer, CRMUserCreateSerializer, CRMUserUpdateSerializer
from apps.utils.serializers import EmptySerializer
from apps.utils.views import BaseViewSet


class CRMUserViewSet(BaseViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    serializer_class = CRMUserSerializer

    permission_classes = [IsAdmin]

    queryset = CRMUser.objects.all()

    serializers = {
        'create': CRMUserCreateSerializer,
        'update': CRMUserUpdateSerializer,
        'destroy': EmptySerializer,
    }

    def check_permissions(self, request):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().check_permissions(request)

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()

    def perform_destroy(self, instance):
        pk = self.kwargs['pk']
        crm_user = CRMUser.objects.filter(pk=pk).first()
        CRMUser.objects.filter(pk=pk).update(deleted=True)
        User.objects.filter(pk=crm_user.user.pk).update(deleted=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        serializer = CRMUserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        headers = self.get_success_headers(serializer.data)
        serializer = CRMUserSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
