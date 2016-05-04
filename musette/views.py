# -*- coding: UTF-8 -*-
import datetime
import json
import redis

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import defaultfilters
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from .forms import (
    FormAddTopic, FormEditTopic,
    FormAddComment, FormEditProfile
)
from .models import (
    Category, Forum, Topic,
    Comment, Notification, Register,
    AbstractProfile
)
from .utils import (
    remove_folder_attachment,
    get_users_topic, get_notifications,
    remove_file, get_route_file,
    get_photo_profile, get_main_model_profile,
    get_app_model, get_count_fields_model
)


class ForumsView(View):

    '''
        This view display all forum registered
    '''
    template_name = "musette/index.html"

    def get(self, request, *args, **kwargs):

        categories = Category.objects.filter(hidden=False)

        data = {
            'categories': categories
        }

        return render(request, self.template_name, data)


class ForumView(View):

    '''
        This view display one forum registered
    '''

    def get(self, request, forum, *args, **kwargs):

        template_name = "musette/forum_index.html"
        page_template = "musette/forum.html"

        forum = get_object_or_404(Forum, name=forum, hidden=False)
        topics = Topic.objects.filter(
            forum_id=forum.idforum).order_by("-is_top", "-date")

        # Get forum childs
        forums_childs = Forum.objects.filter(parent=forum, hidden=False)

        iduser = request.user.id
        if iduser:
            try:
                Register.objects.get(
                    forum_id=forum.idforum, user_id=iduser
                )
                register = True
            except Register.DoesNotExist:
                register = False

        else:
            register = False

        data = {
            'forum': forum,
            'forums_childs': forums_childs,
            'topics': topics,
            'register': register
        }

        if request.is_ajax():
            template_name = page_template

        return render(request, template_name, data)


class TopicView(View):

    '''
        This view display one Topic of forum
    '''

    def get(self, request, forum, slug, idtopic, *args, **kwargs):

        template_name = "musette/topic_index.html"
        page_template = "musette/topic.html"

        forum = get_object_or_404(Forum, name=forum, hidden=False)
        topic = get_object_or_404(Topic, idtopic=idtopic, slug=slug)

        form_comment = FormAddComment()

        comments = Comment.objects.filter(topic_id=idtopic)

        photo = get_photo_profile(topic.user.id)

        data = {
            'topic': topic,
            'form_comment': form_comment,
            'comments': comments,
            'photo': photo
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)


class NewTopicView(FormView):

    '''
        This view allowed add new topic
    '''
    template_name = "musette/new_topic.html"
    form_class = FormAddTopic

    def get_success_url(self):
        return '/forum/' + self.kwargs['forum']

    def get(self, request, forum, *args, **kwargs):

        data = {
            'form': self.form_class,
            'forum': forum,
        }
        return render(request, self.template_name, data)

    def post(self, request, forum, *args, **kwargs):

        form = FormAddTopic(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            now = datetime.datetime.now()
            user = User.objects.get(id=request.user.id)
            forum = get_object_or_404(Forum, name=forum)
            title = strip_tags(request.POST['title'])

            obj.date = now
            obj.user = user
            obj.forum = forum
            obj.title = title
            obj.slug = defaultfilters.slugify(request.POST['title'])

            if 'attachment' in request.FILES:
                id_attachment = get_random_string(length=32)
                obj.id_attachment = id_attachment

                file_name = request.FILES['attachment']
                obj.attachment = file_name

            if forum.is_moderate:
                if forum.moderators_id == request.user.id:
                    obj.moderate = True
                else:
                    obj.moderate = False

                    # Send email to moderator
                    if settings.SITE_URL.endswith("/"):
                        site = settings.SITE_URL + "forum/" + forum.name
                    else:
                        site = settings.SITE_URL + "/forum/" + forum.name

                    title_email = "New notification " + settings.SITE_NAME
                    message = "You have one new topic: " + site
                    email_from = settings.EMAIL_MUSETTE
                    user_moderator = get_object_or_404(
                        User, id=forum.moderators_id
                    )
                    email_moderator = user_moderator.email
                    if email_from:
                        send_mail(
                            title_email, message, email_from,
                            [email_moderator], fail_silently=False
                        )
            else:
                obj.moderate = True

            obj.save()
            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Form invalid"))
            return self.form_invalid(form, **kwargs)


class EditTopicView(FormView):

    '''
        This view allowed edit topic
    '''
    template_name = "musette/edit_topic.html"
    form_class = FormEditTopic

    def get_success_url(self):
        return '/forum/' + self.kwargs['forum']

    def get(self, request, forum, idtopic, *args, **kwargs):

        topic = get_object_or_404(
            Topic, idtopic=idtopic, user_id=request.user.id
        )

        # Init fields form
        form = FormEditTopic(instance=topic)

        data = {
            'form': form,
            'forum': forum,
            'topic': topic,
        }

        return render(request, self.template_name, data)

    def post(self, request, forum, idtopic, *args, **kwargs):

        topic = get_object_or_404(
            Topic, idtopic=idtopic, user_id=request.user.id
        )
        file_name = topic.attachment

        form = FormEditTopic(request.POST, request.FILES, instance=topic)
        file_path = settings.MEDIA_ROOT

        if form.is_valid():

            obj = form.save(commit=False)

            title = strip_tags(request.POST['title'])
            description = strip_tags(request.POST['description'])
            slug = defaultfilters.slugify(request.POST['title'])

            obj.title = title
            obj.description = description
            obj.slug = slug

            # If check field clear, remove file when update
            if 'attachment-clear' in request.POST:
                route_file = get_route_file(file_path, file_name.name)

                try:
                    remove_file(route_file)
                except Exception:
                    pass

            if 'attachment' in request.FILES:

                if not topic.id_attachment:
                    id_attachment = get_random_string(length=32)
                    obj.id_attachment = id_attachment

                file_name_post = request.FILES['attachment']
                obj.attachment = file_name_post

                # Route previous file
                route_file = get_route_file(file_path, file_name.name)

                try:
                    # If a previous file exists it removed
                    remove_file(route_file)
                except Exception:
                    pass

            # Update topic
            form.save()

            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Form invalid"))
            return self.form_invalid(form, **kwargs)


class DeleteTopicView(View):

    '''
        This view will delete one topic
    '''

    def get(self, request, forum, idtopic, *args, **kwargs):

        # Previouly verify that exists the topic
        topic = get_object_or_404(
            Topic, idtopic=idtopic, user_id=request.user.id
        )

        iduser_topic = topic.user_id

        # If my user delete
        if request.user.id == iduser_topic:
            remove_folder_attachment(idtopic)
            Topic.objects.filter(
                idtopic=idtopic, user_id=iduser_topic).delete()
        else:
            raise Http404

        return redirect('forum', forum)


class NewCommentView(View):

    '''
        This view allowed add new comment to topic
    '''

    def get(self, request, forum, slug, idtopic, *args, **kwargs):
        raise Http404()

    def post(self, request, forum, slug, idtopic, *args, **kwargs):

        form = FormAddComment(request.POST)

        param = ""
        param = forum + "/" + slug
        param = param + "/" + str(idtopic) + "/"
        url = '/topic/' + param

        if form.is_valid():
            obj = form.save(commit=False)

            now = datetime.datetime.now()
            user = User.objects.get(id=request.user.id)
            topic = get_object_or_404(Topic, idtopic=idtopic)

            obj.date = now
            obj.user = user
            obj.topic_id = topic.idtopic

            obj.save()

            r = redis.StrictRedis()

            idcomment = obj.idcomment

            # Data for notification real time
            comment = Comment.objects.get(idcomment=idcomment)
            username = request.user.username

            # Get photo profile
            photo = get_photo_profile(request.user.id)

            # Data for notification real time
            description = Truncator(comment.description).chars(100)

            # Send notifications
            lista_us = get_users_topic(topic, request.user.id)
            lista_email = []

            # If not exists user that create topic, add
            user_original_topic = topic.user.id
            user_email = topic.user.email

            if not user_original_topic in lista_us:
                lista_us.append(user_original_topic)
                lista_email.append(user_email)
            else:
                user_original_topic = None

            for user in lista_us:
                if user_original_topic != request.user.id:
                    notification = Notification(
                        iduser=user, is_view=False,
                        idobject=idcomment, date=now,
                        is_topic=False, is_comment=True
                    )
                    notification.save()

            # Send email notification
            if settings.SITE_URL.endswith("/"):
                site = settings.SITE_URL[:-1]
            else:
                site = settings.SITE_URL

            title_email = "New notification " + settings.SITE_NAME
            message = "You have one new comment in the topic: " + site + url
            email_from = settings.EMAIL_MUSETTE
            if email_from:
                send_mail(
                    title_email, message, email_from,
                    lista_email, fail_silently=False
                )

            data = {
                "description": description,
                "topic": comment.topic.title,
                "idtopic": comment.topic.idtopic,
                "slug": comment.topic.slug,
                "settings_static": settings.STATIC_URL,
                "username": username,
                "forum": forum,
                "lista_us": lista_us,
                "photo": photo
            }

            json_data = json.dumps(data)
            r.publish('notifications', json_data)

            return HttpResponseRedirect(url)
        else:
            messages.error(request, _("Field required"))
            return HttpResponseRedirect(url)


class EditCommentView(View):

    '''
        This view allowed edit comment to topic
    '''

    def get(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):
        raise Http404()

    def post(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):

        param = ""
        param = forum + "/" + slug
        param = param + "/" + str(idtopic) + "/"
        url = '/topic/' + param

        description = request.POST.get('update_description')

        if description:

            iduser = request.user.id
            Comment.objects.filter(idcomment=idcomment, user=iduser).update(
                description=description
            )

            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)


class DeleteCommentView(View):

    '''
        This view allowed remove comment to topic
    '''

    def get(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):
        raise Http404()

    def post(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):

        param = ""
        param = forum + "/" + slug
        param = param + "/" + str(idtopic) + "/"
        url = '/topic/' + param

        try:
            iduser = request.user.id
            Comment.objects.filter(idcomment=idcomment, user=iduser).delete()
            Notification.objects.filter(idobject=idcomment).delete()

            return HttpResponseRedirect(url)
        except Exception:
            return HttpResponseRedirect(url)


class AllNotification(View):

    '''
        This view return all notification
        and paginate
    '''

    def get(self, request, *args, **kwargs):

        template_name = "musette/all_notification_index.html"
        page_template = "musette/all_notification.html"

        iduser = request.user.id

        Notification.objects.filter(iduser=iduser).update(is_view=True)

        notifications = get_notifications(iduser)
        data = {
            'notifications': notifications,
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)


def SetNotifications(request):
    '''
        This view set all views notifications in true
    '''
    iduser = request.user.id
    Notification.objects.filter(iduser=iduser).update(is_view=True)

    return HttpResponse("Ok")


class AddRegisterView(View):

    '''
        This view add register to forum
    '''

    def get(self, request, forum, *args, **kwargs):
        raise Http404()

    def post(self, request, forum, *args, **kwargs):

        url = '/forum/' + forum + "/"

        forum = get_object_or_404(Forum, name=forum, hidden=False)
        idforum = forum.idforum
        iduser = request.user.id
        date = datetime.datetime.now()

        register = Register(
            forum_id=idforum, user_id=iduser,
            date=date
        )
        register.save()
        return HttpResponseRedirect(url)


class UnregisterView(View):

    '''
        This view remove register to forum
    '''

    def get(self, request, forum, *args, **kwargs):
        raise Http404()

    def post(self, request, forum, *args, **kwargs):

        url = '/forum/' + forum + "/"

        forum = get_object_or_404(Forum, name=forum, hidden=False)
        idforum = forum.idforum
        iduser = request.user.id

        Register.objects.filter(
            forum_id=idforum, user_id=iduser,
        ).delete()

        return HttpResponseRedirect(url)


class UsersForumView(View):

    '''
        This view display users register in forum
    '''
    def get(self, request, forum, *args, **kwargs):

        template_name = "musette/users_forum_index.html"
        page_template = "musette/users_forum.html"

        forum = get_object_or_404(Forum, name=forum, hidden=False)
        registers = Register.objects.filter(forum_id=forum.idforum)

        data = {
            'forum': forum,
            'registers': registers,
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)

    def post(self, request, forum, *args, **kwargs):
        raise Http404()


class TopicSearch(View):

    '''
        This view django, display results of search of topics
    '''

    def get(self, request, forum, *args, **kwargs):

        template_name = "musette/topic_search_index.html"
        page_template = "musette/topic_search.html"

        search = request.GET.get('q')

        forum = get_object_or_404(Forum, name=forum)
        idforum = forum.idforum

        topics = Topic.objects.filter(
            forum_id=idforum, title__icontains=search
        )

        data = {
            'topics': topics,
            'forum': forum,
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)


class ProfileView(View):

    '''
        This view django, display results of the profile
    '''

    def get(self, request, username, *args, **kwargs):
        template_name = "musette/profile.html"

        user = get_object_or_404(User, username=username)
        iduser = user.id

        # Get model extend Profile
        ModelProfile = get_main_model_profile()

        # Get name app of the extend model Profile
        app = get_app_model(ModelProfile)

        # Check if the model profile is extended
        count_fields_model = get_count_fields_model(ModelProfile)
        count_fields_abstract = get_count_fields_model(AbstractProfile)
        if count_fields_model > count_fields_abstract:
            model_profile_is_extend = True
        else:
            model_profile_is_extend = False
        profile = get_object_or_404(ModelProfile, iduser=iduser)

        photo = get_photo_profile(iduser)

        data = {
            'profile': profile,
            'photo': photo,
            'user': request.user,
            'app': app,
            'model_profile_is_extend': model_profile_is_extend
        }

        return render(request, template_name, data)


class EditProfileView(FormView):

    '''
        This view allowed edit profile
    '''
    template_name = "musette/edit_profile.html"
    form_class = FormEditProfile

    def get_success_url(self):
        return '/profile/' + self.kwargs['username']

    def get(self, request, username, *args, **kwargs):

        ModelProfile = get_main_model_profile()
        profile = get_object_or_404(
            ModelProfile, iduser=request.user.id
        )

        # Init fields form
        form = FormEditProfile(instance=profile)

        data = {
            'form': form
        }

        return render(request, self.template_name, data)

    def post(self, request, username, *args, **kwargs):

        ModelProfile = get_main_model_profile()
        profile = get_object_or_404(
            ModelProfile, iduser=request.user.id
        )

        file_name = profile.photo

        form = FormEditProfile(request.POST, request.FILES, instance=profile)
        file_path = settings.MEDIA_ROOT

        if form.is_valid():

            obj = form.save(commit=False)

            about = strip_tags(request.POST['about'])

            obj.about = about

            # If check field clear, remove file when update
            if 'attachment-clear' in request.POST:
                route_file = get_route_file(file_path, file_name.name)

                try:
                    remove_file(route_file)
                except Exception:
                    pass

            if 'attachment' in request.FILES:

                if not obj.id_attachment:
                    id_attachment = get_random_string(length=32)
                    obj.id_attachment = id_attachment

                file_name_post = request.FILES['photo']
                obj.photo = file_name_post

                # Route previous file
                route_file = get_route_file(file_path, file_name.name)

                try:
                    # If a previous file exists it removed
                    remove_file(route_file)
                except Exception:
                    pass

            # Update profile
            form.save()

            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Form invalid"))
            return self.form_invalid(form, **kwargs)