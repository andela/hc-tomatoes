from django.contrib import admin
from hc.blog.models import Post, Category

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

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
