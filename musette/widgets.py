from django import forms


class TextareaWidget(forms.Textarea):
    """
    Widget rich textarea
    """
    class Media:
        # tiny_mce
        js = ('//cdn.tinymce.com/4/tinymce.min.js',
              '/static/musette/js/textareas.js')
