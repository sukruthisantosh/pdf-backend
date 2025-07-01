from django.contrib import admin
from .models import PDF

@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'uploaded_at', 'file')
    list_filter = ('uploaded_at',)
    search_fields = ('original_name',)
    readonly_fields = ('uploaded_at',) 