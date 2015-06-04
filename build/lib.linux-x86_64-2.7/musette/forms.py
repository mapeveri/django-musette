# encoding:utf-8

from django import forms
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .utils import basename
from .models import Topic, Comment
from .widgets import TextareaWidget


class FormAdminTopic(forms.ModelForm):
	'''
	Form for topic cadmin
	'''
	class Meta:
		model = Topic
		exclude = ('slug', 'id_attachment')
		widgets = {
			'description': TextareaWidget,
		}


class FormAddTopic(forms.ModelForm):
	'''
	Form for create one new topic
	'''

	class Meta:
		model = Topic
		exclude = ('forum', "user", "slug", "date", "id_attachment", "moderate")
		widgets = {
			'description': TextareaWidget,
		}

	def __init__(self, *args, **kwargs):

		super(FormAddTopic, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			if key != "attachment":
				self.fields[key].required = True
				self.fields[key].widget.attrs['class'] = class_css
			else:
				self.fields[key].required = False


class CustomClearableFileInput(ClearableFileInput):
	'''
	  Changes order fields
	'''
	template_with_initial = (
		'%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
		'%(clear_template)s<br />%(input_text)s: %(input)s'
	)
	template_with_clear = '<br>  <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'

	def render(self, name, value, attrs=None):
		substitutions = {
			'initial_text': self.initial_text,
			'input_text': self.input_text,
			'clear_template': '',
			'clear_checkbox_label': self.clear_checkbox_label,
		}
		template = '%(input)s'
		substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

		if self.is_initial(value):
			template = self.template_with_initial
			substitutions.update(self.get_template_substitution_values(value))

			values = self.get_template_substitution_values(value)
			initial = basename(values['initial'])

			if not self.is_required:
				checkbox_name = self.clear_checkbox_name(name)
				checkbox_id = self.clear_checkbox_id(checkbox_name)
				substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
				substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
				substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
				substitutions['clear_template'] = self.template_with_clear % substitutions
				substitutions['initial'] = conditional_escape(initial)

		return mark_safe(template % substitutions)


class FormEditTopic(forms.ModelForm):
	'''
	Form for edit one new topic
	'''

	class Meta:
		model = Topic
		exclude = ('forum', "user", "slug", "date", "id_attachment", "moderate")
		widgets = {
			'description': TextareaWidget,
			'attachment': CustomClearableFileInput,
		}

	def __init__(self, *args, **kwargs):

		super(FormEditTopic, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			if key != "attachment":
				self.fields[key].required = True
				self.fields[key].widget.attrs['class'] = class_css
			else:
				self.fields[key].required = False


class FormAddComment(forms.ModelForm):
	'''
	Form for add comment to topic
	'''
	class Meta:
		model = Comment
		fields = ['description']
		widgets = {
			'description': TextareaWidget,
		}

	def __init__(self, *args, **kwargs):

		super(FormAddComment, self).__init__(*args, **kwargs)

		for key in self.fields:
			if key == "description":
				self.fields[key].required = True
				self.fields[key].widget.attrs['style'] = "width: 100%"
