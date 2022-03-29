from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.timesince import timesince
from django_rest_passwordreset.models import ResetPasswordToken

from Users.models import Profile
from Users.models import User


# remove these lines if you want these models on admin
admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'first_name', 'is_verified', 'is_premium')
    list_display_links = ('id', 'email')
    list_filter = ('is_admin', 'is_verified', 'is_premium')
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'phone_number')},
        ),
        ('Account status', {'fields': ('is_verified', 'is_premium')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at', 'id']
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    search_fields = ('email', 'id')
    ordering = ('id', 'email', 'first_name')
    filter_horizontal = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'gender', 'birth_date')
    list_display_links = ('nickname',)
    list_filter = ('gender', 'birth_date')
    fieldsets = (
        (None, {'fields': ('user',)}),
        (
            'Personal info',
            {'fields': ('profile_image', 'birth_date', 'gender')},
        ),
        ('Account info', {'fields': ('nickname', 'bio')}),
    )
    search_fields = ('nickname', 'id')
    ordering = ('user', 'nickname', 'gender', 'birth_date')


class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'object',
        'action_flag',
        'change_message',
        'modified',
    )
    readonly_fields = ['object', 'modified']
    search_fields = ('user__email',)
    date_hierarchy = 'action_time'
    list_filter = ('action_flag', 'content_type__model')
    list_per_page = 20

    def object(self, obj):
        url = obj.get_admin_url()
        object_repr = obj.object_repr
        model = obj.content_type.model
        return format_html(f'<a href="{url}">{object_repr} [{model}]</a>')

    def modified(self, obj):
        if not obj.action_time:
            return 'Never'
        return f'{timesince(obj.action_time)} ago'

    modified.admin_order_field = 'action_time'


admin.site.register(User, UserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Profile, ProfileAdmin)
