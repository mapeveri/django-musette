import base64
import json
import redis
from itertools import chain

from django.db.models import F, Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    password_reset, password_reset_complete,
    password_reset_confirm
)
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.template import defaultfilters
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.translation import ugettext_lazy as _

from musette import forms, models, utils


class LoginView(FormView):
    """
    Login View
    """
    template_name = "musette/login.html"
    form_class = forms.FormLogin
    success_url = reverse_lazy("forums")

    def get(self, request, *args, **kwargs):
        # Check if is logged, if is trur redirect to home
        if request.user.is_authenticated():
            return ForumsView.as_view()(request)
        else:
            # No is logged, redirecto index login
            data = {
                'form': self.form_class
            }
            return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Check if is authenticated and form valid
        if not request.user.is_authenticated():
            if form.is_valid():
                # This method is one method of class
                # FormLogin in forms.py and is the
                # responsible of authenticate to user
                user = form.form_authenticate()
                if user:
                    if user.is_active:
                        # Login is correct
                        login(request, user)
                        return redirect("forums")
                    else:
                        messages.error(request, _("The user is not active"))
                        return self.form_invalid(form, **kwargs)
                else:
                    return self.form_invalid(form, **kwargs)
            else:
                return self.form_invalid(form, **kwargs)
        else:
            return redirect("forums")


class LogoutView(View):
    """
    View logout
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)

        return redirect("forums")


class SignUpView(FormView):
    """
    This view is responsible of
    create one new user
    """
    template_name = "musette/signup.html"
    form_class = forms.FormSignUp
    success_url = reverse_lazy("signup")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("forums")
        else:
            data = {'form': self.form_class}
            return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not request.user.is_authenticated():
            if form.is_valid():
                form.create_user()
                msj = _(
                    "Registration was successful. Please, check your email "
                    "to validate the account."
                )
                messages.success(request, msj)
                return self.form_valid(form, **kwargs)
            else:
                messages.error(request, _("Invalid form"))
                return self.form_invalid(form, **kwargs)
        else:
            return redirect("forums")


class ConfirmEmailView(View):
    """
    Form confirm email
    """
    template_name = "musette/confirm_email.html"

    def get(self, request, username, activation_key, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("forums")

        # Decoding username
        username = base64.b64decode(username.encode("utf-8")).decode("ascii")
        # Parameters for template
        data = {'username': username}

        # Get model profile
        ModelProfile = utils.get_main_model_profile()

        # Check if not expired key
        user_profile = get_object_or_404(
            ModelProfile, activation_key=activation_key
        )

        if user_profile.key_expires < timezone.now():
            return render(request, "musette/confirm_email_expired.html", data)

        # Active user
        User = get_user_model()
        user = get_object_or_404(User, username=username)
        user.is_active = True
        user.save()
        return render(request, self.template_name, data)


class NewKeyActivationView(View):
    """
    View for get a new key activation
    """
    template_name = "musette/confirm_email_expired.html"

    def post(self, request, username, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("forums")

        User = get_user_model()
        user = get_object_or_404(User, username=username)
        email = user.email

        # For confirm email
        data = utils.get_data_confirm_email(email)

        # Get model profile
        ModelProfile = utils.get_main_model_profile()

        # Update activation key
        profile = get_object_or_404(ModelProfile, iduser=user)
        profile.activation_key = data['activation_key']
        profile.key_expires = data['key_expires']
        profile.save()

        # Send email for confirm user
        utils.send_welcome_email(email, username, data['activation_key'])
        data = {'username': username, 'new_key': True}
        return render(request, self.template_name, data)


def reset_password(request):
    """
    This view contains the form
    for reset password of user
    """
    if request.user.is_authenticated():
        return redirect("forums")

    if request.method == "POST":
        messages.success(request, _('Please, check your email'))

    return password_reset(
        request,
        template_name='musette/password_reset_form.html',
        email_template_name='musette/password_reset_email.html',
        subject_template_name='musette/password_reset_subject.txt',
        password_reset_form=PasswordResetForm,
        token_generator=default_token_generator,
        post_reset_redirect='password_reset',
        from_email=None,
        extra_context=None,
        html_email_template_name=None
    )


def reset_pass_confirm(request, uidb64, token):
    """
    This view display form reset confirm pass
    """
    if request.user.is_authenticated():
        return redirect("forums")

    return password_reset_confirm(
        request, uidb64=uidb64, token=token,
        template_name='musette/password_reset_confirm.html',
        token_generator=default_token_generator,
        set_password_form=SetPasswordForm,
        post_reset_redirect=None,
        extra_context=None
    )


def reset_done_pass(request):
    """
    This view display messages
    that successful reset pass
    """
    if request.user.is_authenticated():
        return redirect("forums")

    return password_reset_complete(
        request, extra_context=None,
        template_name='musette/password_reset_complete.html',
    )


class ForumsView(View):
    """
    This view display all forum registered
    """
    template_name = "musette/index.html"

    def get(self, request, *args, **kwargs):
        # Get categories that not hidden
        categories = models.Category.objects.filter(hidden=False)

        data = {
            'categories': categories
        }

        return render(request, self.template_name, data)


class ForumView(View):
    """
    This view display one forum registered
    """
    def get(self, request, category, forum, *args, **kwargs):

        template_name = "musette/forum_index.html"
        page_template = "musette/forum.html"

        # Get topics forum
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum, hidden=False
        )
        topics = models.Topic.objects.filter(
            forum_id=forum.idforum
        ).order_by("-is_top", "-last_activity", "-date")

        # Get forum childs
        forums_childs = models.Forum.objects.filter(parent=forum, hidden=False)

        iduser = request.user.id
        if iduser:
            try:
                models.Register.objects.get(
                    forum_id=forum.idforum, user_id=iduser
                )
                register = True
            except models.Register.DoesNotExist:
                register = False

        else:
            register = False

        # Get messages for forum
        now = timezone.now()
        message_queryset = forum.message_information.filter(
            Q(message_expires_from__lte=now, message_expires_to__gte=now),
            Q(message_expires_to__hour__lte=now.hour)
        )

        # Get if has message and if is correct, get message
        if message_queryset.count() > 0:
            has_message_forum = True
            message_forum = message_queryset[0].message_information
        else:
            has_message_forum = False
            message_forum = ""

        data = {
            'forum': forum,
            'forums_childs': forums_childs,
            'topics': topics,
            'register': register,
            'has_message_forum': has_message_forum,
            'message_forum': message_forum
        }

        if request.is_ajax():
            template_name = page_template

        return render(request, template_name, data)


class TopicView(View):
    """
    This view display one Topic of forum
    """
    def get(self, request, category, forum, slug, idtopic, *args, **kwargs):

        template_name = "musette/topic_index.html"
        page_template = "musette/topic.html"

        # Get topic
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum, hidden=False
        )
        topic = get_object_or_404(models.Topic, idtopic=idtopic, slug=slug)

        # Form for comments
        form_comment = forms.FormAddComment()

        # Get comments of the topic
        comments = models.Comment.objects.filter(topic_id=idtopic)

        # Get photo of created user topic
        photo = utils.get_photo_profile(topic.user.id)

        # Get suggest topic
        words = topic.title.split(" ")
        condition = Q()
        for word in words:
            condition |= Q(title__icontains=word)

        suggest = models.Topic.objects.filter(condition).exclude(
            idtopic=topic.idtopic
        )[:10]

        data = {
            'topic': topic,
            'form_comment': form_comment,
            'comments': comments,
            'photo': photo,
            'suggest': suggest
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)


class NewTopicView(FormView):
    """
    This view allowed add new topic
    """
    template_name = "musette/new_topic.html"
    form_class = forms.FormAddTopic

    def get_success_url(self):
        return reverse_lazy(
            'forum', kwargs={
                'category': self.kwargs['category'],
                'forum': self.kwargs['forum']
            }
        )

    def get_context_data(self, **kwargs):
        context = super(NewTopicView, self).get_context_data(**kwargs)
        context['forum'] = self.kwargs['forum']
        context['category'] = self.kwargs['category']
        return context

    def get(self, request, category, forum, *args, **kwargs):

        data = {
            'form': self.form_class,
            'forum': forum,
            'category': category,
        }
        return render(request, self.template_name, data)

    def post(self, request, category, forum, *args, **kwargs):
        # Form new topic
        form = forms.FormAddTopic(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)

            now = timezone.now()
            User = get_user_model()
            user = User.objects.get(id=request.user.id)
            # Get forum
            forum = get_object_or_404(
                models.Forum, category__name=category, name=forum
            )
            title = conditional_escape(request.POST['title'])

            obj.date = now
            obj.user = user
            obj.forum = forum
            obj.title = title
            obj.slug = defaultfilters.slugify(request.POST['title'])

            # If has attachment
            if 'attachment' in request.FILES:
                id_attachment = get_random_string(length=32)
                obj.id_attachment = id_attachment

                file_name = request.FILES['attachment']
                obj.attachment = file_name

            # If the forum is moderate
            if forum.is_moderate:
                # If is moderator, so the topic is moderate
                if request.user in forum.moderators.all():
                    obj.moderate = True
                elif request.user.is_superuser:
                    obj.moderate = True
                else:
                    obj.moderate = False

                    # Get moderators forum
                    for moderator in forum.moderators.all():
                        # Send email to moderator
                        if settings.SITE_URL.endswith("/"):
                            site = settings.SITE_URL + "forum/" + forum.name
                        else:
                            site = settings.SITE_URL + "/forum/" + forum.name

                        # Send email
                        form.send_mail_topic(site, moderator.email)
            else:
                obj.moderate = True

            # Save topic
            obj.save()

            # Get moderators forum
            list_us = []
            for moderator in forum.moderators.all():
                # If not is my user
                if moderator.id != request.user.id:
                    # Send notification to moderator
                    related_object = ContentType.objects.get_for_model(obj)
                    notification = models.Notification(
                        iduser=moderator.id, is_view=False,
                        idobject=obj.idtopic, date=now,
                        is_topic=True, is_comment=False,
                        content_type=related_object
                    )
                    notification.save()
                    list_us.append(moderator.id)

            # Get photo profile
            username = request.user.username
            photo = utils.get_photo_profile(request.user.id)

            # Data necessary for realtime
            data = {
                "topic": obj.title,
                "idtopic": obj.idtopic,
                "slug": obj.slug,
                "settings_static": settings.STATIC_URL,
                "username": username,
                "forum": forum.name,
                "category": forum.category.name,
                "list_us": list_us,
                "photo": photo
            }

            # Add to real time new notification
            json_data_notification = json.dumps(data)
            # Redis instance
            r = redis.StrictRedis()
            # Publish
            r.publish('notifications', json_data_notification)

            messages.success(
                request, _("The topic '%(topic)s' was successfully created")
                % {'topic': obj.title}
            )
            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Invalid form"))
            return self.form_invalid(form, **kwargs)


class EditTopicView(FormView):
    """
    This view allowed edit topic
    """
    template_name = "musette/edit_topic.html"
    form_class = forms.FormEditTopic

    def get_success_url(self):
        return reverse_lazy(
            'forum', kwargs={
                'category': self.kwargs['category'],
                'forum': self.kwargs['forum']
            }
        )

    def get_context_data(self, **kwargs):
        context = super(EditTopicView, self).get_context_data(**kwargs)
        context['forum'] = self.kwargs['forum']
        context['category'] = self.kwargs['category']
        return context

    def get(self, request, category, forum, idtopic, *args, **kwargs):
        # Get topic
        topic = get_object_or_404(
            models.Topic, idtopic=idtopic, user_id=request.user.id
        )

        # Init fields form
        form = forms.FormEditTopic(instance=topic)

        data = {
            'form': form,
            'forum': forum,
            'topic': topic,
            'category': category,
        }

        return render(request, self.template_name, data)

    def post(self, request, category, forum, idtopic, *args, **kwargs):
        # Get topic
        topic = get_object_or_404(
            models.Topic, idtopic=idtopic, user_id=request.user.id
        )
        file_name = topic.attachment

        # Get form
        form = forms.FormEditTopic(request.POST, request.FILES, instance=topic)
        file_path = settings.MEDIA_ROOT

        if form.is_valid():

            obj = form.save(commit=False)

            title = conditional_escape(request.POST['title'])
            slug = defaultfilters.slugify(request.POST['title'])

            obj.title = title
            obj.slug = slug

            # If check field clear, remove file when update
            if 'attachment-clear' in request.POST:
                route_file = utils.get_route_file(file_path, file_name.name)

                try:
                    utils.remove_file(route_file)
                except Exception:
                    pass

            # If has attachment
            if 'attachment' in request.FILES:

                if not topic.id_attachment:
                    id_attachment = get_random_string(length=32)
                    obj.id_attachment = id_attachment

                file_name_post = request.FILES['attachment']
                obj.attachment = file_name_post

                # Route previous file
                route_file = utils.get_route_file(file_path, file_name.name)

                try:
                    # If a previous file exists it removed
                    utils.remove_file(route_file)
                except Exception:
                    pass

            # Update topic
            form.save()

            messages.success(
                request,
                _("The topic '%(topic)s' was successfully edited")
                % {'topic': obj.title}
            )
            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Invalid form"))
            return self.form_invalid(form, **kwargs)


class DeleteTopicView(View):
    """
    This view will delete one topic
    """
    def delete(self, request, *args, **kwargs):

        # Dict delete
        qd = QueryDict(request.body)
        DELETE_DICT = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}

        # Get params
        forum = DELETE_DICT.get("forum")
        idtopic = DELETE_DICT.get("idtopic")

        # Previouly verify that exists the topic
        topic = get_object_or_404(
            models.Topic, idtopic=idtopic, user_id=request.user.id
        )

        # Get data topic
        iduser_topic = topic.user_id
        title_topic = topic.title

        # If my user so delete
        if request.user.id == iduser_topic:
            utils.remove_folder_attachment(idtopic)
            models.Topic.objects.filter(
                idtopic=idtopic, user_id=iduser_topic
            ).delete()
            messages.success(
                request, _("The topic '%(topic)s' was successfully deleted")
                % {'topic': title_topic}
            )
        else:
            raise HttpResponse(status=404)

        return HttpResponse(status=200)


class OpenCloseTopicView(View):
    """
    This view close or re-open topic
    """
    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        userid = int(request.POST.get("userid"))
        idtopic = int(request.POST.get("idtopic"))
        is_close = int(request.POST.get("is_close"))

        # Check if has params
        if idtopic and userid:
            # Only same user can close topic
            if request.user.id == userid:
                status = True if is_close == 1 else False
                # Close or re-open topic
                models.Topic.objects.filter(idtopic=idtopic).update(
                    is_close=status
                )

                return HttpResponse(status=200)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)


class LikeUnlikeTopicView(View):
    """
    This view like or unlike topic
    """
    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        idtopic = int(request.POST.get("idtopic"))
        is_like = int(request.POST.get("is_like"))

        # Get topic
        topic = get_object_or_404(models.Topic, idtopic=idtopic)

        # If is like
        if is_like == 1:
            # Like topic
            models.Topic.objects.filter(idtopic=idtopic).update(
                like=F('like') + 1
            )
            # Add reference
            models.LikeTopic.objects.create(
                topic=topic, user=request.user
            )
        else:
            # Like topic
            models.Topic.objects.filter(idtopic=idtopic).update(
                like=F('like') - 1
            )
            # Delete reference
            models.LikeTopic.objects.filter(
                topic=topic, user=request.user
            ).delete()

        return HttpResponse(status=200)


class LikeUnlikeCommentView(View):
    """
    This view like or unlike comment
    """
    def get(self, request, *args, **kwargs):
        return Http404()

    def post(self, request, *args, **kwargs):
        idcomment = int(request.POST.get("idcomment"))
        is_like = int(request.POST.get("is_like"))

        # Get comment
        comment = get_object_or_404(models.Comment, idcomment=idcomment)

        # If is like
        if is_like == 1:
            # Like comment
            models.Comment.objects.filter(idcomment=idcomment).update(
                like=F('like') + 1
            )
            # Add reference
            models.LikeComment.objects.create(
                comment=comment, user=request.user
            )
        else:
            # Like comment
            models.Comment.objects.filter(idcomment=idcomment).update(
                like=F('like') - 1
            )
            # Delete reference
            models.LikeComment.objects.filter(
                comment=comment, user=request.user
            ).delete()

        return HttpResponse(status=200)


class NewCommentView(View):
    """
    This view allowed add new comment to topic
    """
    def get(self, request, category, forum, slug, idtopic, *args, **kwargs):
        raise Http404()

    def post(self, request, category, forum, slug, idtopic, *args, **kwargs):
        # Form new comment
        form = forms.FormAddComment(request.POST)

        url = reverse_lazy('topic', kwargs={
            'category': category, 'forum': forum,
            'slug': slug, 'idtopic': str(idtopic)
        })

        if form.is_valid():
            obj = form.save(commit=False)

            # Save new comment
            now = timezone.now()
            User = get_user_model()
            user = User.objects.get(id=request.user.id)
            topic = get_object_or_404(models.Topic, idtopic=idtopic)
            obj.date = now
            obj.user = user
            obj.topic_id = topic.idtopic
            obj.save()

            # Update last activity TopicSearch
            models.Topic.objects.filter(idtopic=idtopic).update(
                last_activity=now
            )

            # Data for notification real time
            idcomment = obj.idcomment
            comment = models.Comment.objects.get(idcomment=idcomment)
            username = request.user.username

            # Get photo profile
            photo = utils.get_photo_profile(request.user.id)

            # Send notifications
            list_us = utils.get_users_topic(topic, request.user.id)
            lista_email = []

            # If not exists user that create topic, add
            user_original_topic = topic.user.id
            user_email = topic.user.email

            if not (user_original_topic in list_us):
                list_us.append(user_original_topic)
                lista_email.append(user_email)
            else:
                user_original_topic = None

            # Get content type for comment model
            related_object_type = ContentType.objects.get_for_model(comment)
            for user in list_us:
                if user_original_topic != request.user.id:
                    notification = models.Notification(
                        iduser=user, is_view=False,
                        idobject=idcomment, date=now,
                        is_topic=False, is_comment=True,
                        content_type=related_object_type
                    )
                    notification.save()

            # Send email notification
            if settings.SITE_URL.endswith("/"):
                site = settings.SITE_URL[:-1]
            else:
                site = settings.SITE_URL

            # Send email
            form.send_mail_comment(site, str(url), lista_email)

            # Data necessary for realtime
            data = {
                "topic": comment.topic.title,
                "idtopic": comment.topic.idtopic,
                "slug": comment.topic.slug,
                "settings_static": settings.STATIC_URL,
                "username": username,
                "forum": forum,
                "category": comment.topic.forum.category.name,
                "photo": photo
            }

            # Add item for notification
            data_notification = data
            data_notification['list_us'] = list_us

            # Add to real time new notification
            json_data_notification = json.dumps(data_notification)
            # Redis instance
            r = redis.StrictRedis()
            # Publish
            r.publish('notifications', json_data_notification)

            # Publish new comment in topic
            data_comment = data
            data_comment['description'] = comment.description
            json_data_comment = json.dumps(data_comment)
            r.publish('comments', json_data_comment)

            messages.success(request, _("Added new comment"))
            return HttpResponseRedirect(url)
        else:
            messages.error(request, _("Field required"))
            return HttpResponseRedirect(url)


class EditCommentView(View):
    """
    This view allowed edit comment to topic
    """
    def get(self, request, category, forum, slug, idtopic, idcomment,
            *args, **kwargs):
        raise Http404()

    def post(self, request, category, forum, slug, idtopic, idcomment,
             *args, **kwargs):

        url = reverse_lazy('topic', kwargs={
            'category': category, 'forum': forum,
            'slug': slug, 'idtopic': str(idtopic)
        })

        # Valid if has description
        description = request.POST.get('update_description')
        if description:
            # Edit comment
            iduser = request.user.id
            models.Comment.objects.filter(
                idcomment=idcomment, user=iduser
            ).update(
                description=description
            )

            messages.success(request, _("Comment edited"))
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)


class DeleteCommentView(View):
    """
    This view allowed remove comment to topic
    """
    def get(self, request, category, forum, slug, idtopic, idcomment,
            *args, **kwargs):
        raise Http404()

    def post(self, request, category, forum, slug, idtopic, idcomment,
             *args, **kwargs):

        url = reverse_lazy('topic', kwargs={
            'category': category, 'forum': forum,
            'slug': slug, 'idtopic': str(idtopic)
        })

        # Delete comment and notification
        try:
            iduser = request.user.id
            models.Comment.objects.filter(
                idcomment=idcomment, user=iduser
            ).delete()

            messages.success(request, _("Comment deleted"))
            return HttpResponseRedirect(url)
        except Exception:
            return HttpResponseRedirect(url)


class AllNotification(View):
    """
    This view return all notification and paginate
    """
    def get(self, request, *args, **kwargs):
        template_name = "musette/all_notification_index.html"
        page_template = "musette/all_notification.html"

        iduser = request.user.id

        # Set all notification like view
        models.Notification.objects.filter(iduser=iduser).update(
            is_view=True
        )

        # Get all notification user
        notifications = utils.get_notifications(iduser)
        data = {
            'notifications': notifications,
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)


def SetNotifications(request):
    """
    This view set all views notifications in true
    """
    iduser = request.user.id
    models.Notification.objects.filter(iduser=iduser).update(is_view=True)

    return HttpResponse("Ok")


class AddRegisterView(View):
    """
    This view add register to forum
    """
    def get(self, request, category, forum, *args, **kwargs):
        raise Http404()

    def post(self, request, category, forum, *args, **kwargs):
        url = reverse_lazy(
            'forum', kwargs={'category': category, 'forum': forum}
        )

        # Get data
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum, hidden=False
        )
        idforum = forum.idforum
        iduser = request.user.id
        date = timezone.now()

        # Add new register
        register = models.Register(
            forum_id=idforum, user_id=iduser,
            date=date
        )
        register.save()
        messages.success(request, _("You have successfully registered"))
        return HttpResponseRedirect(url)


class UnregisterView(View):
    """
    This view remove register to forum
    """
    def get(self, request, category, forum, *args, **kwargs):
        raise Http404()

    def post(self, request, category, forum, *args, **kwargs):
        url = reverse_lazy(
            'forum', kwargs={'category': category, 'forum': forum}
        )

        # Get data
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum, hidden=False
        )
        idforum = forum.idforum
        iduser = request.user.id

        # Remove register
        models.Register.objects.filter(
            forum_id=idforum, user_id=iduser,
        ).delete()

        messages.success(request, _("Registration was successfully canceled"))
        return HttpResponseRedirect(url)


class UsersForumView(View):
    """
    This view display users register in forum
    """
    def get(self, request, category, forum, *args, **kwargs):

        template_name = "musette/users_forum_index.html"
        page_template = "musette/users_forum.html"

        # Get register users
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum, hidden=False
        )
        moderators = forum.moderators.all()
        # Get registers, exclude moderators
        registers = forum.register_forums.filter(~Q(user__in=moderators))

        # Add moderator to users
        users = list(chain(registers, moderators))

        data = {
            'forum': forum,
            'users': users,
        }

        if request.is_ajax():
            template_name = page_template
        return render(request, template_name, data)

    def post(self, request, forum, *args, **kwargs):
        raise Http404()


class TopicSearch(View):
    """
    This view django, display results of search of topics
    """
    def get(self, request, category, forum, *args, **kwargs):
        template_name = "musette/topic_search_index.html"
        page_template = "musette/topic_search.html"

        # Get param to search
        search = request.GET.get('q')

        # Get id forum
        forum = get_object_or_404(
            models.Forum, category__name=category, name=forum
        )
        idforum = forum.idforum

        # Search topics
        topics = models.Topic.objects.filter(
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
    """
    This view django, display results of the profile
    """
    def get(self, request, username, *args, **kwargs):
        template_name = "musette/profile.html"

        # Get user param
        User = get_user_model()
        user = get_object_or_404(User, username=username)
        iduser = user.id

        # Get model extend Profile
        ModelProfile = utils.get_main_model_profile()

        # Get name app of the extend model Profile
        app = utils.get_app_model(ModelProfile)

        # Check if the model profile is extended
        count_fields_model = utils.get_count_fields_model(ModelProfile)
        count_fields_abstract = utils.get_count_fields_model(
            models.AbstractProfile
        )
        if count_fields_model > count_fields_abstract:
            model_profile_is_extend = True
        else:
            model_profile_is_extend = False
        profile = get_object_or_404(ModelProfile, iduser=iduser)

        photo = utils.get_photo_profile(iduser)

        # Get last topic of the profile
        topics = models.Topic.objects.filter(user=user)[:5]

        data = {
            'profile': profile,
            'photo': photo,
            'user': request.user,
            'topics': topics,
            'app': app,
            'model_profile_is_extend': model_profile_is_extend
        }

        return render(request, template_name, data)


class EditProfileView(FormView):
    """
    This view allowed edit profile
    """
    template_name = "musette/edit_profile.html"
    form_class = forms.FormEditProfile

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={
            'username': self.kwargs['username']
        })

    def get(self, request, username, *args, **kwargs):

        ModelProfile = utils.get_main_model_profile()
        profile = get_object_or_404(
            ModelProfile, iduser=request.user.id
        )

        # Init fields form
        form = forms.FormEditProfile(instance=profile)

        data = {
            'form': form
        }

        return render(request, self.template_name, data)

    def post(self, request, username, *args, **kwargs):

        ModelProfile = utils.get_main_model_profile()
        profile = get_object_or_404(
            ModelProfile, iduser=request.user.id
        )

        file_name = profile.photo

        form = forms.FormEditProfile(
            request.POST, request.FILES, instance=profile
        )
        file_path = settings.MEDIA_ROOT

        if form.is_valid():

            obj = form.save(commit=False)
            about = request.POST['about']
            obj.about = about

            # If check field clear, remove file when update
            if 'attachment-clear' in request.POST:
                route_file = utils.get_route_file(file_path, file_name.name)

                try:
                    utils.remove_file(route_file)
                except Exception:
                    pass

            if 'attachment' in request.FILES:

                if not obj.id_attachment:
                    id_attachment = get_random_string(length=32)
                    obj.id_attachment = id_attachment

                file_name_post = request.FILES['photo']
                obj.photo = file_name_post

                # Route previous file
                route_file = utils.get_route_file(file_path, file_name.name)

                try:
                    # If a previous file exists it removed
                    utils.remove_file(route_file)
                except Exception:
                    pass

            # Update profile
            form.save()

            messages.success(
                request,
                _("Your profile was successfully edited")
            )
            return self.form_valid(form, **kwargs)
        else:
            messages.error(request, _("Invalid form"))
            return self.form_invalid(form, **kwargs)


class IsTrollView(View):
    """
    Set if a user is troll
    """
    def get(self, request, *args, **kwargs):
        raise Http404()

    def post(self, request, *args, **kwargs):
        user_post = request.POST.get('username')
        check = True if int(request.POST.get('check')) == 1 else False

        # Get troll
        User = get_user_model()
        username = get_object_or_404(User, username=user_post)

        # Check if is user correct
        total = utils.get_total_forum_moderate_user(username)
        if not username.is_superuser and total == 0:
            # Is a troll
            ModelProfile = utils.get_main_model_profile()
            ModelProfile.objects.filter(iduser=username).update(is_troll=check)

        return redirect(
            "profile", username=user_post
        )
