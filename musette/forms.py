from django import forms
from django.conf import settings
from django.contrib.auth import (
    authenticate, get_user_model, password_validation
)
from django.contrib.staticfiles import finders
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from musette import models, utils, widgets
from musette.email import send_mail


class FormLogin(forms.Form):
    """
    Form of login
    """
    widgetUser = forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': _("Username")
    })
    widgetPass = forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': ("Password")
    })
    username = forms.CharField(
        max_length=45, widget=widgetUser, required=True
    )
    password = forms.CharField(
        max_length=45, widget=widgetPass, required=True
    )
    hidden_error = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': ''})

    def form_authenticate(self):
        """
        This method if responsible of authenticate user login, if ok
        then return the user
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            error = ""
            error = error + "<ul class='errorlist'><li>"
            error = error + str(_("Username or password incorrect."))
            error = error + "</li></ul>"
            self._errors["hidden_error"] = error

        return user


class FormSignUp(forms.ModelForm):
    """
    Form for create one new user
    """
    widget_pass = forms.PasswordInput(attrs={'class': 'form-control'})
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    pass_confirm = forms.CharField(max_length=128, widget=widget_pass)

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'password'
        ]

    def __init__(self, *args, **kwargs):
        super(FormSignUp, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': ''})
        class_css = 'form-control'

        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['class'] = class_css

            if key is "username":
                self.fields[key].widget.attrs['placeholder'] = _("Username")
            elif key is "email":
                self.fields[key].widget.attrs['placeholder'] = _("Email")
            elif key is "first_name":
                self.fields[key].widget.attrs['placeholder'] = _("Names")
            elif key is "last_name":
                self.fields[key].widget.attrs['placeholder'] = _("Surname")
            elif key is "password":
                self.fields[key].widget.attrs['placeholder'] = _("Password")
            elif key is "pass_confirm":
                placeholder = _("Repeat password")
                self.fields[key].widget.attrs['placeholder'] = placeholder

    # Valid the passwords
    def clean_pass_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('pass_confirm')
        if password1 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        # Check if password is very easy
        password_validation.validate_password(password2, self.instance)
        return password2

    # Valid the email that is unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        User = get_user_model()
        count = User.objects.filter(
            email=email
        ).exclude(username=username).count()

        if email and count:
            raise forms.ValidationError(_('Email addresses must be unique.'))
        return email

    # Create one new user
    def create_user(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        now = timezone.now()

        # Create user
        User = get_user_model()
        us = User(
            username=username, email=email,
            first_name=first_name,
            last_name=last_name, is_active=False,
            is_superuser=False, date_joined=now,
            is_staff=False
        )
        us.set_password(password)
        us.save()


class FormAdminTopic(forms.ModelForm):
    """
    Form for topic cadmin
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FormAdminTopic, self).__init__(*args, **kwargs)

        if not self.request.user.is_superuser:
            queryset = models.Forum.objects.filter(
                moderators=self.request.user
            )
            self.fields['forum'].queryset = queryset

    class Meta:
        model = models.Topic
        exclude = ('slug', 'id_attachment')
        widgets = {
            'description': widgets.TextareaWidget,
        }


class FormAddTopic(forms.ModelForm):
    """
    Form for create one new topic
    """
    class Meta:
        model = models.Topic
        exclude = (
            "forum", "user", "slug", "date",
            "id_attachment", "moderate", "is_top"
            "is_close",
        )
        widgets = {
            'description': widgets.TextareaWidget,
        }

    def __init__(self, *args, **kwargs):
        super(FormAddTopic, self).__init__(*args, **kwargs)
        class_css = 'form-control'

        for key in self.fields:
            if key != "attachment":
                if key == "title" or key == "description":
                    self.fields[key].required = True
                    self.fields[key].widget.attrs['v-model'] = key
                    self.fields[key].widget.attrs['class'] = class_css
                    self.fields[key].widget.attrs['required'] = 'required'
            else:
                self.fields[key].required = False

    def send_mail_topic(self, site, email_moderator):
        site_name = settings.SITE_NAME
        title_email = _("New topic in %(site)s ") % {'site': site_name}
        message = _("You have one new topic to moderate: %(site)s") % {
            'site': site
        }
        email_from = settings.EMAIL_MUSETTE

        if email_from:
            send_mail(
                title_email, message, email_from,
                [email_moderator], fail_silently=False
            )


class CustomClearableFileInput(ClearableFileInput):
    """
    Changes order fields
    """
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )
    template_with_clear = ""
    template_with_clear = '<br>  <label for="%(clear_checkbox_id)s"> '
    template_with_clear += ' %(clear_checkbox_label)s</label> %(clear)s'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(
            ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))

            values = self.get_template_substitution_values(value)
            initial = utils.basename(values['initial'])

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)

                substitutions['clear_checkbox_name'] = conditional_escape(
                    checkbox_name)

                substitutions['clear_checkbox_id'] = conditional_escape(
                    checkbox_id)

                substitutions['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})

                clear_template = self.template_with_clear % substitutions
                substitutions['clear_template'] = clear_template
                substitutions['initial'] = conditional_escape(initial)

        return mark_safe(template % substitutions)


class FormEditTopic(forms.ModelForm):
    """
    Form for edit one new topic
    """
    class Meta:
        model = models.Topic
        exclude = (
            "forum", "user", "slug", "date",
            "id_attachment", "moderate", "is_top",
            "is_close",
        )
        widgets = {
            'description': widgets.TextareaWidget,
            'attachment': CustomClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super(FormEditTopic, self).__init__(*args, **kwargs)
        class_css = 'form-control'

        for key in self.fields:
            if key != "attachment":
                if key == "title" or key == "description":
                    v_init = ""
                    v_init += key + "=" + "'"
                    v_init += str(kwargs['instance'].title) + "'"
                    self.fields[key].required = True
                    self.fields[key].widget.attrs['v-model'] = key
                    self.fields[key].widget.attrs['value'] = v_init
                    self.fields[key].widget.attrs['class'] = class_css
                    self.fields[key].widget.attrs['required'] = 'required'
            else:
                self.fields[key].required = False


class FormAddComment(forms.ModelForm):
    """
    Form for add comment to topic
    """
    class Meta:
        model = models.Comment
        fields = ['description']
        widgets = {
            'description': widgets.TextareaWidget,
        }

    def __init__(self, *args, **kwargs):
        super(FormAddComment, self).__init__(*args, **kwargs)

        for key in self.fields:
            if key == "description":
                self.fields[key].required = True
                self.fields[key].widget.attrs['style'] = "width: 100%"
                self.fields[key].widget.attrs['v-model'] = key
                self.fields[key].widget.attrs['required'] = 'required'

    def send_mail_comment(self, site, url, lista_email):
        title_email = _("New comment in %(site)s") % {
            'site': settings.SITE_NAME
        }

        message = _("You have one new comment in the topic: %(site)s") % {
            'site': site + url
        }

        email_from = settings.EMAIL_MUSETTE
        if email_from:
            send_mail(
                title_email, message, email_from,
                lista_email, fail_silently=False
            )


class FormAdminProfile(forms.ModelForm):
    """
    Form for admin profile
    """
    class Meta:
        model = utils.get_main_model_profile()
        exclude = (
            'idprofile', 'iduser',
        )
        widgets = {
            'about': widgets.TextareaWidget,
        }


class FormEditProfile(forms.ModelForm):
    """
    Form for edit one profile
    """
    class Meta:
        model = utils.get_main_model_profile()
        exclude = (
            'idprofile', 'iduser', 'activation_key',
            'key_expires'
        )
        widgets = {
            'about': widgets.TextareaWidget,
            'photo': CustomClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super(FormEditProfile, self).__init__(*args, **kwargs)
        class_css = 'form-control'

        for key in self.fields:
            self.fields[key].widget.attrs['class'] = class_css


class FormAdminConfiguration(forms.ModelForm):
    """
    Form configuration
    """
    name_file_custom = finders.find('musette/css/custom.css')

    class Meta:
        model = models.Configuration
        exclude = (
            'idconfig',
        )

    def __init__(self, *args, **kwargs):
        # Read css custom
        file_custom = open(self.name_file_custom, 'r')
        file_custom = file_custom.read()

        # Override init value on edit
        initial = kwargs.get('initial', {})
        initial['custom_css'] = file_custom
        kwargs['initial'] = initial
        super(FormAdminConfiguration, self).__init__(*args, **kwargs)

        # Init value to new record
        self.fields['custom_css'].initial = file_custom

    def save(self, commit=True):
        instance = super(FormAdminConfiguration, self).save(commit=False)

        # Save content in the file
        with open(self.name_file_custom, "w") as text_file:
            text_file.write(instance.custom_css)

        if commit:
            instance.save()
        return instance
