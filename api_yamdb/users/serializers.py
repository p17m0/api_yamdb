from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserLogInSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'bio',
                  'username',
                  'email',
                  'role')

    def validate(self, attrs):
        if 'username' in attrs:
            if attrs['username'] == 'me':
                raise serializers.ValidationError(
                    {'username': 'not me and without @'}
                )
        if 'email' in attrs:
            if '@' not in attrs['email']:
                raise serializers.ValidationError(
                    {'email': 'mail must have @'}
                )
        return attrs


class UserAuthSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
