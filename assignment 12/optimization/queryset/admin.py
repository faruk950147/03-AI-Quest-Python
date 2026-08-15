from django.contrib import admin
from queryset.models import Author, Tag, Post, Comment

# ==============================
# Author Admin
# ==============================
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'updated_at']
    search_fields = ['name', 'email']  # search support

admin.site.register(Author, AuthorAdmin)


# ==============================
# Tag Admin
# ==============================
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Tag, TagAdmin)


# ==============================
# Comment Inline for Post Admin
# ==============================
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # number of empty forms for adding new comments
    readonly_fields = ['created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'content', 'created_at', 'updated_at']
    search_fields = ['content']
    list_filter = ['post', 'created_at']
admin.site.register(Comment, CommentAdmin)

# ==============================
# Post Admin
# ==============================
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'content', 'get_tags', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'author__name']
    list_filter = ['author', 'tags', 'created_at']
    inlines = [CommentInline]

    def get_tags(self, obj):
        """Show all tags for a post in admin list view"""
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"


admin.site.register(Post, PostAdmin)


