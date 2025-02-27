from django.contrib import admin
from .models import HtmlTemplate
# Register your models here.
from .models import ControlPanel  # Исправлено на правильное имя класса
from ckeditor.widgets import CKEditorWidget
from django import forms
from tinymce.widgets import TinyMCE

admin.site.register(ControlPanel)  # Регистрация модели с кастомным админом

class HtmlTemplateForm(forms.ModelForm):
    class Meta:
        model = HtmlTemplate
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30, 'config': 'default'}),  # Используем полную конфигурацию
        }

class HtmlTemplateAdmin(admin.ModelAdmin):
    form = HtmlTemplateForm
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(HtmlTemplate, HtmlTemplateAdmin)