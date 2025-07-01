from django.db import models

class PDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    original_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.original_name
    
    class Meta:
        ordering = ['-uploaded_at'] 