from django.contrib import admin

from .models import Publication, Article, About


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'enable', 'remarks')
    list_display_links = ('id', 'title')

    list_filter = ('topic',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lang', 'create_time', 'enable', 'author', 'publication')
    list_display_links = ('id', 'title')
    list_filter = ('lang', 'create_time')

    list_select_related = ('publication',)
    raw_id_fields = ('publication',)

    class Media:
        js = [
            '/static/tinymce/TinyMCEAdminV5.js'
        ]


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'create_time', 'modify_time')
    list_display_links = ('id',)

    class Media:
        js = [
            '/static/tinymce/TinyMCEAdminV5.js'
        ]
