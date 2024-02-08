from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url')  # 按顺序显示这三个字段

admin.site.register(Page, PageAdmin)
