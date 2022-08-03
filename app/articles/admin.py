from django.contrib import admin

from app.articles.models import Article, Tag

admin.site.register(Tag)
admin.site.register(Article)
