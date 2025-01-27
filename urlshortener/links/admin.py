from datetime import timedelta

from django.contrib import admin
from .models import Link
from django.contrib import admin
from .models import Link
from django.utils.timezone import now



class LinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_id', 'created_at', 'last_accessed', 'user', 'is_unused')
    actions = ['delete_unused_links']

    def is_unused(self, obj):
        return obj.is_unused(days=30)
    is_unused.boolean = True

    def delete_unused_links(self, request, queryset):
        queryset.filter(last_accessed__lt=now() - timedelta(days=30)).delete()
        self.message_user(request, "Неиспользуемые ссылки были удалены.")

admin.site.register(Link, LinkAdmin)
