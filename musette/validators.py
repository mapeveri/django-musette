from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def valid_extension_image(value):
    """
    Function that valid extension when upload file in form.

    Args:
        value (obj): Upload file object.
    """
    if (not value.name.endswith('.png') and
            not value.name.endswith('.jpeg') and
            not value.name.endswith('.gif') and
            not value.name.endswith('.bmp') and
            not value.name.endswith('.jpg')):

        text = _("Files allowed")
        files = ".jpg, .jpeg, .png, .gif, .bmp"
        raise ValidationError(text + ': ' + files)