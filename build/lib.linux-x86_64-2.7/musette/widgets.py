from django import forms


class TextareaWidget(forms.Textarea):

	'''
	Widget rich textarea
	'''
	class Media:
		# tiny_mce
		js = ('/static/js/libs/tiny_mce/tiny_mce.js', '/static/js/textareas.js')