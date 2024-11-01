from rest_framework import serializers
from apps.users.models import User, CRMUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class CRMUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = CRMUser
        fields = (
            'id',
            'name',
            'username',
            'role',
        )

    def get_username(self, obj):
        return obj.user.username


class CRMUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25, required=True)

    class Meta:
        model = CRMUser
        fields = (
            'username',
            'password',
            'name',
            'role',
        )

    def to_internal_value(self, data):
        user_internal = {}

        internal = super().to_internal_value(data)

        for key in UserSerializer.Meta.fields:
            if key in internal:
                user_internal[key] = internal.pop(key)

        internal['user'] = user_internal

        return internal

    def save(self, **kwargs):
        user_data = self.validated_data.pop('user')
        user = User.objects.create(**user_data)
        crm_user = CRMUser.objects.create(user=user, **self.validated_data)
        user.set_password(user_data['password'])
        user.save()
        crm_user.save()
        return crm_user


class CRMUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)

    class Meta:
        model = CRMUser
        fields = (
            'username',
            'password',
            'name',
            'role',
        )

    def to_internal_value(self, data):
        user_internal = {}

        internal = super().to_internal_value(data)

        for key in UserSerializer.Meta.fields:
            if key in internal:
                user_internal[key] = internal.pop(key)

        internal['user'] = user_internal

        return internal

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)
