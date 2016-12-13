from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from musette import models, utils
from musette.api import serializers


# ViewSets for user
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


# ViewSets for categiry
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ViewSets for forum
class ForumViewSet(viewsets.ModelViewSet):
    queryset = models.Forum.objects.all()
    serializer_class = serializers.ForumSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ViewSets for topic
class TopicViewSet(viewsets.ModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ViewSets for register
class RegisterViewSet(viewsets.ModelViewSet):
    queryset = models.Register.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ViewSets for comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


# ViewSets for profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = utils.get_main_model_profile().objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
