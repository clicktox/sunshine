from django.contrib import admin
from models import *

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django.db import transaction
from members.forms import *
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.contrib.auth.forms import AdminPasswordChangeForm
class MemberWebsiteAdmin(admin.ModelAdmin):
    pass
admin.site.register(MemberWebsite, MemberWebsiteAdmin)

class MemberAddressAdmin(admin.ModelAdmin):
    list_display = ('member','street','city','territory','country','postal_code')
admin.site.register(MemberAddress,MemberAddressAdmin)

class MemberAddressInline(admin.StackedInline):
    model = MemberAddress

from members.forms import UserCreationForm,UserChangeForm
class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'email','password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email','password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','avatar')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls import patterns
        return patterns('',
            (r'^(\d+)/password/$',
             self.admin_site.admin_view(self.user_change_password))
        ) + super(UserAdmin, self).get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(UserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters()
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)

    @sensitive_post_parameters()
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context, current_app=self.admin_site.name)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(UserAdmin, self).response_add(request, obj,
                                                   post_url_continue)

class MemberAdmin(UserAdmin):
    inlines = [MemberAddressInline,]
    #form = 

admin.site.register(User, MemberAdmin)

"""
class InsiderInline(admin.StackedInline):
    model = Insider   

class MustHaveContributorInline(admin.TabularInline):
    model = MustHaveContributor   
class InsiderAdmin(admin.ModelAdmin):
    list_display = ('user','joined_on')
    readonly_fields = ('user',)
admin.site.register(Insider,InsiderAdmin)
"""



"""
class InsiderProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(InsiderProduct,InsiderProductAdmin)
admin.site.register(InsiderProductStatus)
admin.site.register(InsiderProductReview)

class MemberShareAdmin(admin.ModelAdmin):
    list_display = ('member','medium','shared_on')
    list_filter = ('medium',)
    
    readonly_fields = ('member',)
    
admin.site.register(MemberShare, MemberShareAdmin)
admin.site.register(MemberShareContent)

    
class InsiderCampaignApplicantAdmin(admin.ModelAdmin):
    list_display = ('insider','campaign')
    list_filter = ('campaign',)
    readonly_fields = ('insider','selected_by')
    search_fields = ['insider__user__email','insider__user__username']
    def save_model(self, request, obj, form, change):
        if 'selected_on' in form.changed_data:
            obj.selected_by = request.user
        obj.save()
        
admin.site.register(InsiderCampaignApplicant,InsiderCampaignApplicantAdmin)

class InsiderProductCampaignInline(admin.StackedInline):
    model = InsiderProductCampaign
    
class InsiderCampaignSurveyInline(admin.StackedInline):
    model = InsiderCampaignSurvey
    
class InsiderCampaignImageInline(admin.StackedInline):
    model = InsiderCampaignImage  

class InsiderCampaignAdmin(admin.ModelAdmin):
    exclude = ('created_by',)
    inlines = [InsiderCampaignImageInline,InsiderCampaignSurveyInline,InsiderProductCampaignInline]
    def save_model(self, request, obj, form, change): 
        obj.created_by = request.user
        obj.save()
        
admin.site.register(InsiderCampaign,InsiderCampaignAdmin)
admin.site.register(InsiderCampaignImage)
admin.site.register(MustHaveContributor)

"""


admin.site.register(SocialProfileType)
admin.site.register(MemberSocialProfile)
admin.site.register(Avatar)
class MemberSignatureAdmin(admin.ModelAdmin):
    search_fields = ('member__last_name', )
    list_display = ('member','signature')
    
admin.site.register(MemberSignature,MemberSignatureAdmin)



    

