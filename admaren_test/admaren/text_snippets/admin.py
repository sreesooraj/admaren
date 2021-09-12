from django.contrib import admin
from text_snippets.models import Title, Text


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', "title")
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', "user", "title", "text_snippet")


admin.site.register(Text, TextAdmin)

admin.site.register(Title, TitleAdmin)