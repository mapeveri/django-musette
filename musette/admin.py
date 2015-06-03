from django.db import router
from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_deleted_objects
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .forms import FormAdminTopic
from .models import Category, Forum, Topic, Comment

from .utils import remove_folder_attachment


class TopicAdmin(admin.ModelAdmin):
	form = FormAdminTopic
	list_display = ('title', 'forum', 'date')
	list_filter = ['title', 'date']
	search_fields = ['title']
	actions=['delete_topic']

	def get_actions(self, request):
		actions = super(TopicAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	def delete_topic(self, request, queryset):
		'''
			This method remove topic's selected
			in the admin django. Can remove one
			o more records.
		'''
		if not self.has_delete_permission(request):
			raise PermissionDenied

		if request.POST.get("post"):
			for obj in queryset:
				idtopic = obj.idtopic
				#Remove folder attachment
				remove_folder_attachment(idtopic)
				# Delete record
				Topic.objects.filter(idtopic=idtopic).delete()

			n = queryset.count()
			self.message_user(request, _("Successfully deleted %(count)d record/s.") % {
	                "count": n, }, messages.SUCCESS)

			return None
		else:

			opts = self.model._meta

			if len(queryset) == 1:
				objects_name = force_text(opts.verbose_name)
			else:
				objects_name = force_text(opts.verbose_name_plural)

			using = router.db_for_write(self.model)

			deletable_objects, model_count, perms_needed, protected = get_deleted_objects(
				queryset, opts, request.user, self.admin_site, using)

			context = {
	            'title': "",
	            'delete_topic': [queryset],
	            'ids': queryset.values_list("idtopic"),
	            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
	            'opts': opts,
	            'objects_name': objects_name,
	            'deletable_objects': [deletable_objects],
        	}

			return TemplateResponse(
	        	request, 'musette/admin/confirm_delete.html',
	        	context, current_app=self.admin_site.name
	        )

	delete_topic.short_description = _("Delete selected %(verbose_name_plural)s")


class ForumAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'escape_html_description', 'topics_count')
	list_filter = ['name', 'category']
	search_fields = ['name']

	# TinyMCE
	class Media:
		js = ('/static/js/libs/tiny_mce/tiny_mce.js', '/static/js/textareas.js')


admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
