from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from musette import models, utils


# Serializers Users
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
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

    def __init__(self, *args, **kwargs):
        super(TopicSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        # If no is superuser, only forum register or is moderator
        if not user.is_superuser:
            registers = models.Register.objects.filter(user=user)
            self.fields['forum'].queryset = models.Forum.objects.filter(
                Q(moderators__in=[user.id]) | Q(register_forums__in=registers)
            )

            # Only my user
            User = get_user_model()
            self.fields['user'].queryset = User.objects.filter(id=user.id)

    class Meta:
        model = models.Topic
        exclude = (
            'slug', 'date', 'moderate', 'id_attachment', 'is_top',
        )


# Serializers register
class RegisterSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        # If no is superuser, get forum that
        # not is register or not is moderator
        if not user.is_superuser:
            registers = models.Register.objects.filter(user=user)
            self.fields['forum'].queryset = models.Forum.objects.filter(
                ~Q(moderators__in=[user.id]), ~Q(
                    register_forums__in=registers
                )
            )

            # Only my user
            User = get_user_model()
            self.fields['user'].queryset = User.objects.filter(id=user.id)

    class Meta:
        model = models.Register
        exclude = ('date',)


# Serializers comment
class CommentSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_superuser:
            # Only my user
            User = get_user_model()
            self.fields['user'].queryset = User.objects.filter(id=user.id)

    class Meta:
        model = models.Comment
        exclude = ('date',)


# Serializers profile
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = utils.get_main_model_profile()
        fields = '__all__'
