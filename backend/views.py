from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import os
from django.conf import settings
from django.core.files.storage import default_storage
from pdfs.models import PDF

@api_view(["GET"])
def hello(request):
    return JsonResponse({"message": "Hello from Django!"})

@api_view(["GET"])
def list_pdfs(request):
    """Get all previously uploaded PDFs"""
    pdfs = PDF.objects.all()
    data = [
        {
            'id': pdf.id,
            'original_name': pdf.original_name,
            'url': request.build_absolute_uri(pdf.file.url),
            'uploaded_at': pdf.uploaded_at.isoformat()
        }
        for pdf in pdfs
    ]
    return Response(data)

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_pdf(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)
    if not file.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)
    
    # Save the file and create PDF model instance
    save_path = os.path.join('pdfs', file.name)
    file_name = default_storage.save(save_path, file)
    
    # Create PDF model instance to store metadata
    pdf = PDF.objects.create(
        file=file_name,
        original_name=file.name
    )
    
    file_url = settings.MEDIA_URL + file_name
    full_url = request.build_absolute_uri(file_url)

    return JsonResponse({
        'message': f'File "{file.name}" uploaded successfully!',
        'url': full_url,
        'id': pdf.id
    })