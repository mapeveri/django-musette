from django.contrib.auth.models import User
from rest_framework import serializers
from musette import models, utils


# Serializers Users
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'is_superuser', 'first_name', 'last_name',
            'email', 'is_staff', 'is_active', 'date_joined'
        )


# Serializers Categories
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


# Serializers Forum
class ForumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Forum
        fields = '__all__'


# Serializers Topic
class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Topic
        fields = '__all__'


# Serializers register
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Register
        fields = '__all__'


# Serializers comment
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = '__all__'


# Serializers profile
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = utils.get_main_model_profile()
        fields = '__all__'
