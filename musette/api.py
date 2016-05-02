from django.contrib.auth.models import User

from rest_framework import serializers, viewsets, routers

from .models import (
    Category, Forum, Topic,
    Register, Comment
)
from .utils import get_main_model_profile


# Serializers Users
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets for user
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Serializers Categories
class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category


# ViewSets for categiry
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Serializers Forum
class ForumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Forum


# ViewSets for forum
class ForumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


# Serializers Topic
class TopicSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Topic


# ViewSets for topic
class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


# Serializers register
class RegisterSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Register


# ViewSets for register
class RegisterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


# Serializers comment
class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment


# ViewSets for comment
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Serializers profile
class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_main_model_profile()


# ViewSets for profile
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_main_model_profile().objects.all()
    serializer_class = ProfileSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/categories', CategoryViewSet)
router.register(r'api/forums', ForumViewSet)
router.register(r'api/topics', TopicViewSet)
router.register(r'api/registers', RegisterViewSet)
router.register(r'api/comments', CommentViewSet)
router.register(r'api/profiles', ProfileViewSet)