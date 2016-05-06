from django.db import router
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .forms import FormAdminTopic
from .models import (
    Category, Forum, Topic,
    Comment, Register, Configuration
)

from .utils import remove_folder_attachment


class TopicAdmin(admin.ModelAdmin):
    form = FormAdminTopic
    list_display = ('title', 'forum', 'date')
    list_filter = ['title', 'date']
    search_fields = ['title']
    actions = ['delete_topic']

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
        '''
            This method remove topic's selected in the admin django.
            Can remove one o more records.
        '''
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
                request,
                _("Successfully deleted %(count)d record/s.") % {
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
            }

            return TemplateResponse(
                request, 'musette/admin/confirm_delete.html',
                context, current_app=self.admin_site.name
            )

    delete_topic.short_description = _(
        "Delete selected %(verbose_name_plural)s"
    )


class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'escape_html_description',
        'moderators', 'topics_count')
    list_filter = ['name', 'category']
    search_fields = ['name']
    actions = ['delete_topic']

    def get_actions(self, request):
        actions = super(ForumAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_topic(self, request, queryset):
        '''
            This method remove forum selected
            in the admin django. Can remove one
            o more records.
        '''
        if not self.has_delete_permission(request):
            raise PermissionDenied

        if request.POST.get("post"):
            for obj in queryset:
                idforum = obj.idforum

                if not obj.moderators.is_superuser:
                    if obj.moderators:

                        # Return forums that moderating one moderator
                        tot_forum_moderator = Forum.objects.filter(
                            moderators=obj.moderators).count()

                        # Only remove permissions if is moderator one forum
                        if tot_forum_moderator <= 1:
                            try:
                                u = User.objects.get(username=obj.moderators)
                                u.user_permissions.clear()
                            except Exception:
                                pass

                # Delete record
                Forum.objects.filter(idforum=idforum).delete()

            n = queryset.count()
            self.message_user(
                request,
                _("Successfully deleted %(count)d record/s.") % {
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
            }

            return TemplateResponse(
                request, 'musette/admin/confirm_delete.html',
                context, current_app=self.admin_site.name
            )

    delete_topic.short_description = _(
        "Delete selected %(verbose_name_plural)s"
    )

    # TinyMCE
    class Media:
        js = ('/static/js/libs/tiny_mce/tiny_mce.js',
              '/static/js/textareas.js')


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
    list_display = ('idconfig',
        'logo', 'class_main')
    list_filter = ['logo', 'class_main']
    search_fields = ['logo', 'class_main']


admin.site.register(Category)
admin.site.register(Register)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Configuration, ConfigurationAdmin)