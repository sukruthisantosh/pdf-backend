from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
import os
from django.conf import settings
from django.core.files.storage import default_storage

@api_view(["GET"])
def hello(request):
    return JsonResponse({"message": "Hello from Django!"})

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_pdf(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)
    if not file.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)
    
    save_path = os.path.join('pdfs', file.name)
    file_name = default_storage.save(save_path, file)
    file_url = settings.MEDIA_URL + file_name

    return JsonResponse({'message': f'File "{file.name}" uploaded successfully!', 'url': file_url})
