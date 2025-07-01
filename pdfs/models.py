from django.db import models
import json

class PDFFile(models.Model):
    file = models.FileField(upload_to='pdfs/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Annotation(models.Model):
    pdf = models.ForeignKey(PDFFile, on_delete=models.CASCADE, related_name='annotations')
    page_index = models.IntegerField()  # Changed from page_number to match frontend
    quote = models.TextField()  # Selected text
    content = models.TextField()  # Note content
    highlight_areas = models.JSONField()  # Store highlight areas as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['page_index', 'created_at']
    
    def __str__(self):
        return f"{self.pdf.name} - Page {self.page_index + 1} - {self.quote[:50]}"
