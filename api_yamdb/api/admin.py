from django.contrib import admin

from reviews.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date',
    )

    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('text',)


admin.site.register(Comment, CommentAdmin)
