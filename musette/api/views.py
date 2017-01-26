from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from musette import models, utils
from musette.api import serializers
from musette.api.permissions import ForumPermissions


# ViewSets for user
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


# ViewSets for categiry
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


# ViewSets for forum
class ForumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Forum.objects.all()
    serializer_class = serializers.ForumSerializer


# ViewSets for topic
class TopicViewSet(viewsets.ModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ForumPermissions,)

    def create(self, request, **kwargs):
        is_my_user = int(request.data['user']) == request.user.id
        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            forum_id = request.data['forum']
            forum = get_object_or_404(models.Forum, pk=forum_id)
            category = forum.category.name
            # If has permissions
            if utils.user_can_create_topic(category, forum, request.user):
                return super(TopicViewSet, self).create(request, **kwargs)
            else:
                raise PermissionDenied({
                    "message": "You don't have permission to access"
                })
        else:
            raise PermissionDenied({
                    "message": "Not your user"
                })


# ViewSets for register
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = models.Register.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ForumPermissions,)

    def create(self, request, **kwargs):
        is_my_user = int(request.data['user']) == request.user.id
        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            forum_id = request.data['forum']
            exists_register = models.Register.objects.filter(
                pk=forum_id, user=request.user
            )
            # If the register not exists
            if exists_register.count() == 0:
                return super(RegisterViewSet, self).create(request, **kwargs)
            else:
                raise PermissionDenied({
                    "message": "You are already Registered"
                })
        else:
            raise PermissionDenied({
                    "message": "Not your user"
                })


# ViewSets for comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, ForumPermissions,)

    def create(self, request, **kwargs):
        is_my_user = int(request.data['user']) == request.user.id
        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            return super(CommentViewSet, self).create(request, **kwargs)
        else:
            raise PermissionDenied({
                    "message": "Not your user"
                })


# ViewSets for profile
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = utils.get_main_model_profile().objects.all()
    serializer_class = serializers.ProfileSerializer
