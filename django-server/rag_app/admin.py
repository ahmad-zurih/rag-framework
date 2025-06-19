from django.contrib import admin
from .models import ChatLog

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_query_summary', 'response_summary')

    def user_query_summary(self, obj):
        return obj.user_query[:50]

    def response_summary(self, obj):
        return obj.response[:50]

