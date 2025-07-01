"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend.views import hello, upload_pdf
from pdfs.views import get_pdfs, save_annotation, get_annotations, delete_annotation
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/', hello),
    path('api/upload/', upload_pdf),
    path('api/pdfs/', get_pdfs, name='get_pdfs'),
    path('api/annotations/save/', save_annotation, name='save_annotation'),
    path('api/annotations/<int:pdf_id>/', get_annotations, name='get_annotations'),
    path('api/annotations/delete/<int:annotation_id>/', delete_annotation, name='delete_annotation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
