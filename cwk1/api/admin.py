from django.contrib import admin

from .models import NewsStories,Author


# Register your models here.

admin.site.register(NewsStories)
admin.site.register(Author)
