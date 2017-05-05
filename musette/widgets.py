from django import forms
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

from musette import utils


class TextareaWidget(forms.Textarea):
    """
    Widget rich textarea.
    """
    class Media:
        # tiny_mce
        js = ('//cdn.tinymce.com/4/tinymce.min.js',
              static('musette/js/textareas.js'))


class CustomClearableFileInput(ClearableFileInput):
    """
    Changes order fields for to ClearableFileInput.

    - **parameters**:
        :param template_with_initial: Content main that contains the input file
            and link with the current file.
        :param template_with_clear: Content checkbox for clear the current
                file.
    """
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />'
    )
    template_with_clear = ""
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s"> '
    template_with_clear += ' %(clear_checkbox_label)s</label> %(clear)s'

    def render(self, name, value, attrs=None):
        if value:
            initial = utils.basename(value.file.name)
        else:
            initial = None

        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'initial_url': settings.MEDIA_URL + str(value),
            'initial': initial,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(
            ClearableFileInput, self).render(name, value, attrs)

        return mark_safe(template % substitutions)
