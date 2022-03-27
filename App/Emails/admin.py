from django.contrib import admin

from Emails.models import Block
from Emails.models import Email


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


admin.site.register(Email, EmailAdmin)
admin.site.register(Block, BlockAdmin)
