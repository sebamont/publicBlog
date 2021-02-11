from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class SuggestionResource(resources.ModelResource):
    class Meta:
        model = Suggestion

class TagResource(resources.ModelResource):
    class Meta:
        model = Tag

class TypeResource(resources.ModelResource):
    class Meta:
        model = Type


class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'creation_date', 'status')
    list_filter = ('status',)
    resource_class = CategoryResource

class ProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['user']
    list_display = ('user', 'creation_date', 'status')
    list_filter = ('status',)
    resource_class = ProfileResource

class SuggestionAdmin (ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['title', 'author']
    list_display = ('title', 'author', 'category', 'status')
    list_filter = ('status', 'category', 'tag')
    resource_class = SuggestionResource

class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'status')
    list_filter = ('status',)
    resource_class = TagResource

class TypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'status')
    list_filter = ('status',)
    resource_class = TagResource

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Type, TypeAdmin)