from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import MAIL
from users.models import User
from users.permissions import AdminUser
from users.serializers import UserAuthSerializer, UserLogInSerializer


@api_view(['POST'])
def users_login(request):
    serializer = UserLogInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mail = serializer.validated_data["email"]
    username = serializer.validated_data['username']
    user = User.objects.filter(email=mail, username=username).exists()
    if not user:
        user = User.objects.create_user(email=mail, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=MAIL,
            recipient_list=[mail],
        )
        message = {'email': mail, 'username': username}
        return Response(message, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def users_login_token(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = request.validated_data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        acces_token = AccessToken(confirmation_code)
        return Response(acces_token)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLogInSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False)
    def get_me(self, request):
        if request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH' and (request.user.is_admin()
                                          or request.user.is_moderator()):

            serializer = UserLogInSerializer(
                user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserLogInSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'get_me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AdminUser]
        return [permission() for permission in permission_classes]
