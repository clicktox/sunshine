from __future__ import unicode_literals
from members.models import *
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
    

import warnings
from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.html import format_html, format_html_join
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())



class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'] % {
                        'username': self.username_field.verbose_name
                    })
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
    
# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


class BaseRegistrationForm(forms.ModelForm):
    first_name=forms.CharField(max_length=255,required=False)
    last_name=forms.CharField(max_length=255,required=False)
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)),label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email')
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _("This email address is already in use. "
                    "Please supply a different email address."))
        return self.cleaned_data['email']
    
    def save(self, commit=True):
        user = super(BaseRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class BaseUserForm(forms.ModelForm):
    first_name=forms.CharField(max_length=255,required=False)
    last_name=forms.CharField(max_length=255,required=False)
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75)),label=_("E-mail"))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email')
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            existing = User.objects.get(username__iexact=self.cleaned_data['username'])
            if existing and (not existing == self.instance ):
                raise forms.ValidationError(_("A user with that username already exists."))
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']

    
    def clean_email(self):
        """
        Validate that the supplied email address is unique.
        """
        try:
            existing = User.objects.get(email__iexact=self.cleaned_data['email'])
            if existing and (not existing == self.instance ):
                raise forms.ValidationError(
                    _("This email address is already in use. "
                        "Please supply a different email address."))
        except User.DoesNotExist:
            pass
        return self.cleaned_data['email']

class BaseMemberForm(forms.ModelForm):
   
    class Meta:
        model = Member
        fields = ('birthdate',)

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = ('uploaded_by',)
"""
class InsiderForm(forms.ModelForm):
    class Meta:
        model = Insider
        exclude = ('user','joined_on')
"""
class MemberAddressForm(forms.ModelForm):
    class Meta:
        model = MemberAddress
        exclude = ('member','latitude','longitude')
"""
class InsiderProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=((0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')))
    class Meta:
        model = InsiderProductReview
        exclude = ('insider','product','reviewed_on')
"""
class MemberShareContentForm(forms.ModelForm):
    shareon = forms.CharField(max_length=255)
    class Meta:
        model = MemberShareContent
        exclude = ('uuid')
        
        
from django.contrib.auth.forms import ReadOnlyPasswordHashField        
class MemberChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[ \w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "[SPACE]/@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "[SPACE]/@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=254)
    
    class Meta:
        model = User
        exclude = ('password','groups','user_permissions','superuser_status','avatar','slug','is_staff','is_active')
    


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[ \w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "[SPACE]/@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "[SPACE]/@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[ \w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "[SPACE]/@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "[SPACE]/@/./+/-/_ characters.")})
    email = forms.EmailField(label=_("Email"), max_length=254)
   
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username","email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





    
    