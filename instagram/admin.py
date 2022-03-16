from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Post, Comment, Tag

# 1번째 방법
# admin.site.register(Post)

# 2번째 방법
# class PostAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Post, PostAdmin)


# 3번째 방법
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):    
    list_display = ['id', 'photo_tag', 'message', 'is_public', 'created_at', 'updated_at']        
    list_display_links = ['message']
    list_filter = ['created_at']
    search_fields = ['message']    
    
    def photo_tag(self, post):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" style="width: 72px; />')
        return None
    
    def message_length(self, post):
        return f"{len(post.message)}"

@admin.register(Comment)    
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass