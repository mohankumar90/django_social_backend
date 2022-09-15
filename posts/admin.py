from django.contrib import admin

from .models import (Person, Post)
# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display=('user','country')
    list_display_links = (['user'])
    list_editable = (['country'])   
    search_fields=('user',)
    list_per_page = 10

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title', 'created', 'owner')
    search_fields=('owner',)
    list_per_page = 10