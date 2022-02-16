from django.contrib import admin

from Emails.models import Email
from Emails.models import Block


class BlockAdmin(admin.ModelAdmin):
    model = Block


class EmailAdmin(admin.ModelAdmin):
    model = Email


admin.site.register(Email, EmailAdmin)
admin.site.register(Block, BlockAdmin)
