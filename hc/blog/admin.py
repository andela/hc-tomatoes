from django.contrib import admin
from hc.blog.models import Post, Category, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish')
    list_filter = ('author', 'publish')
    date_hierarchy = 'publish'
    ordering = ['publish']
    prepopulated_fields = {'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'text', 'author')
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
