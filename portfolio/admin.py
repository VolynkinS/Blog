from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Projects, Category


class ProjectsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Projects
        fields = '__all__'


class ProjectsAdmin(admin.ModelAdmin):
    form = ProjectsAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'description', 'image', 'get_image', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('get_image', 'views', 'created_at', 'updated_at')
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="175"')

    get_image.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление Проектами'
admin.site.site_header = 'Управление Проектами'
