# -*- coding: UTF-8 -*-
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import defaultfilters
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags

from django.utils.translation import ugettext_lazy as _

from endless_pagination.decorators import page_template
from log.utils import set_error_to_log

from .forms import FormAddTopic, FormEditTopic, FormAddComment
from .models import Category, Forum, Topic, Comment, Notification
from .settings import URL_PROFILE
from .utils import (
	remove_folder_attachment, get_id_profile,
	get_photo_profile, get_users_topic,
	get_notifications, remove_file,
	helper_paginator, get_route_file, remove_folder,
	exists_folder
)


class ForumsView(View):
	'''
	This view display all forum registered
	'''
	template_name = "musette/index.html"

	def get(self, request, *args, **kwargs):

		categories = Category.objects.filter(hidden=False)

		if request.user.id:
			notifications = get_notifications(request.user.id)
		else:
			notifications = None

		data = {
				'categories': categories,
				'notifications': notifications
			}

		return render(request, self.template_name, data)


class ForumView(View):
	'''
	This view display one forum registered
	'''
	template_name = "musette/forum.html"

	def get(self, request, forum, *args, **kwargs):

		forum = get_object_or_404(Forum, name=forum, hidden=False)
		topics = Topic.objects.filter(forum_id=forum.idforum)

		pag = helper_paginator(self, request, topics, 15, 'topics')

		if request.user.id:
			notifications = get_notifications(request.user.id)
		else:
			notifications = None

		data = {
			'forum': forum,
			'topics': pag['topics'],
			'paginator': pag,
			'notifications': notifications,
		}

		return render(request, self.template_name, data)


@page_template('musette/topic.html')
def TopicView(request, forum, slug, idtopic,
	template='musette/topic_index.html', extra_context=None,
	*args, **kwargs):
	'''
	This view display one Topic of forum
	'''

	forum = get_object_or_404(Forum, name=forum, hidden=False)
	topic = get_object_or_404(Topic, idtopic=idtopic, slug=slug)

	profile = get_id_profile(topic.user_id)
	field_photo = get_photo_profile(profile)

	form_comment = FormAddComment()

	comments = Comment.objects.filter(topic_id=idtopic)

	if request.user.id:
		notifications = get_notifications(request.user.id)
	else:
		notifications = None

	data = {
		'topic': topic,
		'profile': profile,
		'URL_PROFILE': URL_PROFILE,
		'field_photo': field_photo,
		'form_comment': form_comment,
		'comments': comments,
		'notifications': notifications,
	}

	if extra_context is not None:
		data.update(extra_context)
	return render(request, template, data)


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

		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)

		# Init fields form
		form = FormEditTopic(instance=topic)

		data = {
			'form': form,
			'topic': topic,
		}

		return render(request, self.template_name, data)

	def post(self, request, forum, idtopic, *args, **kwargs):

		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)
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
		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)

		iduser_topic = topic.user_id

		# If my user delete
		if request.user.id == iduser_topic:
			remove_folder_attachment(idtopic)
			Topic.objects.filter(idtopic=idtopic, user_id=iduser_topic).delete()
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to remove the job ' + str(idtopic)
			error = error +	' of user ' + str(iduser_topic)

			set_error_to_log(request, error)
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

			inserted = obj.save()

			idcomment = obj.idcomment
			lista_us = get_users_topic(topic, request.user.id)
			for user in lista_us:
				notification = Notification(
								iduser=user, is_view=False,
								idobject=idcomment, date=now,
								is_topic=False, is_comment=True
							)
				notification.save()


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

			return HttpResponseRedirect(url)
		except Exception:
			return HttpResponseRedirect(url)


@page_template('musette/all_notification.html')
def AllNotification(request, template='musette/all_notification_index.html',
					extra_context=None, *args, **kwargs):

	iduser = request.user.id

	Notification.objects.filter(iduser=iduser).update(is_view=True)

	notifications = get_notifications(iduser)
	data = {
		'notifications': notifications,
	}

	if extra_context is not None:
		data.update(extra_context)
	return render(request, template, data)


def SetNotifications(request):
	'''
		This view set all views notifications in true
	'''
	iduser = request.user.id
	Notification.objects.filter(iduser=iduser).update(is_view=True)

	return HttpResponse("Ok")
