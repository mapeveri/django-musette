from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from musette import models, realtime, utils
from musette.api import serializers
from musette.api.permissions import ForumPermissions, IsReadOnly


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
    permission_classes = (
        IsAuthenticatedOrReadOnly, ForumPermissions,
    )

    def get_permissions(self):
        # If is troll then only is read only
        if self.request.user.is_authenticated():
            if self.request.user.user.is_troll:
                self.permission_classes = [IsReadOnly, ]
        return super(TopicViewSet, self).get_permissions()

    def perform_create(self, serializer):
        request = self.request
        is_my_user = int(request.data['user']) == request.user.id

        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            forum_id = request.data['forum']
            forum = get_object_or_404(models.Forum, pk=forum_id)
            category = forum.category.name
            # If has permissions
            if utils.user_can_create_topic(category, forum, request.user):
                # Save the record topic
                if serializer.is_valid():
                    # If the forum is moderate send email
                    serializer = utils.check_moderate_topic_email(
                        request, forum, serializer
                    )
                    # Save record
                    topic = serializer.save()
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Parameters for realtime
                photo = utils.get_photo_profile(request.user.id)
                username = request.user.username
                forum_name = forum.name

                # Get moderators forum and send notification
                list_us = utils.get_moderators_and_send_notification_topic(
                    request, forum, topic
                )

                # Data necessary for realtime
                data = realtime.data_base_realtime(
                    topic, photo, forum_name, username
                )

                # Send new notification realtime
                realtime.new_notification(data, list_us)

                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
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

    def get_permissions(self):
        # If is troll then only is read only
        if self.request.user.is_authenticated():
            if self.request.user.user.is_troll:
                self.permission_classes = [IsReadOnly, ]
        return super(RegisterViewSet, self).get_permissions()

    def create(self, request, **kwargs):
        is_my_user = int(request.data['user']) == request.user.id
        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            forum_id = request.data['forum']
            exists_register = models.Register.objects.filter(
                forum_id=forum_id, user=request.user
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

    def get_permissions(self):
            # If is troll then only is read only
        if self.request.user.is_authenticated():
            if self.request.user.user.is_troll:
                self.permission_classes = [IsReadOnly, ]
        return super(CommentViewSet, self).get_permissions()

    def perform_create(self, serializer):
        request = self.request
        is_my_user = int(request.data['user']) == request.user.id
        # If is my user or is superuser can create
        if is_my_user or request.user.is_superuser:
            # Save the record comment
            if serializer.is_valid():
                comment = serializer.save()
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            topic_id = request.data['topic']
            topic = get_object_or_404(models.Topic, pk=topic_id)

            # Parameters for notification comments
            photo = utils.get_photo_profile(request.user.id)
            username = request.user.username
            forum = topic.forum.name

            # Send notifications comment
            params = utils.get_users_and_send_notification_comment(
                request, topic, comment
            )
            list_us = params['list_us']
            list_email = params['list_email']

            # Get url for email
            url = reverse_lazy('topic', kwargs={
                'category': topic.forum.category, 'forum': forum,
                'slug': topic.slug, 'idtopic': str(topic.idtopic)
            })

            # Send e    mail
            utils.send_mail_comment(str(url), list_email)

            # Data necessary for realtime
            data = realtime.data_base_realtime(topic, photo, forum, username)

            # Send new notification realtime
            realtime.new_notification(data, list_us)

            # Send new comment in realtime
            comment_description = request.data['description']
            realtime.new_comment(data, comment_description)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            raise PermissionDenied({
                    "message": "Not your user"
                })


# ViewSets for profile
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = utils.get_main_model_profile().objects.all()
    serializer_class = serializers.ProfileSerializer
