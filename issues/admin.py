from django.contrib import admin
from .models import Comment, Issue, Tag


class CommentAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, CommentAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Tag, TagAdmin)