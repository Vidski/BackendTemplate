from django.contrib import admin

from Emails.models import Block
from Emails.models import Email
from Emails.models import Suggestion


class BlockAdmin(admin.ModelAdmin):
    model = Block
    list_display = ('id', 'title', 'show_link')
    list_display_links = ('id', 'title')
    list_filter = (
        'title',
        'show_link',
    )
    fieldsets = (
        ('Content', {'fields': ('id', 'title', 'content')}),
        ('Link', {'fields': ('show_link', 'link_text', 'link')}),
    )
    readonly_fields = [
        'id',
    ]
    search_fields = ('title', 'id', 'link', 'link_text', 'content')


class EmailAdmin(admin.ModelAdmin):
    model = Email
    list_display = (
        'id',
        'subject',
        'to',
        'to_all_users',
        'is_test',
        'was_sent',
    )
    list_filter = ('to', 'to_all_users', 'is_test', 'was_sent')
    fieldsets = (
        ('Content', {'fields': ('id', 'subject', 'header', 'to')}),
        ('Blocks', {'fields': ('blocks',)}),
        (
            'Configuration',
            {'fields': ('to_all_users', 'is_test', 'programed_send_date')},
        ),
        ('Sent information', {'fields': ('was_sent', 'sent_date')}),
    )
    list_display_links = ('id', 'subject')
    readonly_fields = ['id', 'was_sent', 'sent_date']
    search_fields = ('to', 'id', 'subject', 'programed_send_date')
    ordering = ('to_all_users', 'is_test', 'was_sent', 'sent_date', 'to')


class SuggestionAdmin(admin.ModelAdmin):
    model = Suggestion
    list_display = (
        'id',
        'user',
        'get_subject_display',
        'was_sent',
        'was_read',
    )
    list_filter = ('subject', 'user', 'was_read', 'was_sent')

    fieldsets = (
        ('Content', {'fields': ('id', 'user', 'subject', 'header')}),
        ('Blocks', {'fields': ('blocks',)}),
        ('Configuration', {'fields': ('to', 'was_read', 'was_sent')},),
        ('Sent information', {'fields': ('sent_date',)}),
    )
    # list_display_links = ('id', 'subject')
    readonly_fields = ['id', 'was_sent', 'sent_date']
    # search_fields = ('to', 'id', 'subject', 'programed_send_date')
    # ordering = ('to_all_users', 'is_test', 'was_sent', 'sent_date', 'to')


admin.site.register(Email, EmailAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
