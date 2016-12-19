from django.db import router
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .forms import FormAdminConfiguration, FormAdminTopic
from .models import (
    Category, Forum, Topic,
    Comment, Register, Configuration,
    MessageForum
)

from .utils import remove_folder_attachment


class TopicAdmin(admin.ModelAdmin):
    form = FormAdminTopic
    list_display = ('title', 'forum', 'date', 'moderate', 'is_close')
    list_filter = ['title', 'date', 'moderate', 'is_close']
    search_fields = ['title', 'date', 'moderate', 'is_close']
    actions = ['delete_topic']

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(TopicAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    def get_queryset(self, request):
        qs = super(TopicAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        forums = Forum.objects.filter(moderators=request.user.id)
        lista = []
        for f in forums:
            lista.append(f.idforum)

        return qs.filter(forum_id__in=lista)

    def get_actions(self, request):
        actions = super(TopicAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_topic(self, request, queryset):
        """
        This method remove topic's selected in the admin django.
        Can remove one o more records.
        """
        if not self.has_delete_permission(request):
            raise PermissionDenied

        if request.POST.get("post"):
            for obj in queryset:
                idtopic = obj.idtopic
                # Remove folder attachment
                remove_folder_attachment(idtopic)
                # Delete record
                Topic.objects.filter(idtopic=idtopic).delete()

            n = queryset.count()
            self.message_user(
                request, _("Successfully deleted %(count)d record/s.") % {
                    "count": n, }, messages.SUCCESS
            )

            return None
        else:

            opts = self.model._meta

            if len(queryset) == 1:
                objects_name = force_text(opts.verbose_name)
            else:
                objects_name = force_text(opts.verbose_name_plural)

            using = router.db_for_write(self.model)

            del_obj, model_c, perms_n, protected = get_deleted_objects(
                queryset, opts, request.user, self.admin_site, using
            )

            context = {
                'title': "",
                'delete_topic': [queryset],
                'ids': queryset.values_list("idtopic"),
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'opts': opts,
                'objects_name': objects_name,
                'deletable_objects': [del_obj],
                'action': 'delete_topic',
            }

            return TemplateResponse(
                request, 'musette/admin/confirm_delete.html', context
            )

    delete_topic.short_description = _(
        "Delete selected %(verbose_name_plural)s"
    )


class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'forum_description',
        'topics_count', 'is_moderate'
    )
    list_filter = ['name', 'category']
    search_fields = ['name']
    actions = ['delete_forum']

    def get_actions(self, request):
        actions = super(ForumAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_forum(self, request, queryset):
        """
        This method remove forum selected
        in the admin django. Can remove one
        o more records.
        """
        if not self.has_delete_permission(request):
            raise PermissionDenied

        if request.POST.get("post"):
            for obj in queryset:
                idforum = obj.idforum
                # Remove permissions to moderators
                obj.remove_user_permissions_moderator()

                # Delete record
                Forum.objects.filter(idforum=idforum).delete()

            n = queryset.count()
            self.message_user(
                request, _("Successfully deleted %(count)d record/s.") % {
                    "count": n, }, messages.SUCCESS
            )

            return None
        else:

            opts = self.model._meta

            if len(queryset) == 1:
                objects_name = force_text(opts.verbose_name)
            else:
                objects_name = force_text(opts.verbose_name_plural)

            using = router.db_for_write(self.model)

            del_obj, model_c, perms_n, protected = get_deleted_objects(
                queryset, opts, request.user, self.admin_site, using
            )

            context = {
                'title': "",
                'delete_topic': [queryset],
                'ids': queryset.values_list("idforum"),
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'opts': opts,
                'objects_name': objects_name,
                'deletable_objects': [del_obj],
                'action': 'delete_forum'
            }

            return TemplateResponse(
                request, 'musette/admin/confirm_delete.html', context
            )

    delete_forum.short_description = _(
        "Delete selected %(verbose_name_plural)s"
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'topic', 'forum', 'user')
    list_filter = ['topic', 'user']
    search_fields = ['topic', 'user']

    def forum(self, obj):
        return obj.topic.forum
    forum.short_description = 'Forum'
    forum.admin_order_field = 'topic__forum'


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'logo',)
    form = FormAdminConfiguration


class MessageForumAdmin(admin.ModelAdmin):
    list_display = (
        'forum', 'message_information',
        'message_expires_from', 'message_expires_to'
    )


admin.site.register(Category)
admin.site.register(Register)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(MessageForum, MessageForumAdmin)
