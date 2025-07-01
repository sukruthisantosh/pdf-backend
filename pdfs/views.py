from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from django.conf import settings
from .models import PDFFile, Annotation
import os

# Create your views here.

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
    
    # Save PDF to database
    pdf_file = PDFFile.objects.create(
        file=file,
        name=file.name
    )
    
    file_url = request.build_absolute_uri(pdf_file.file.url)
    
    return JsonResponse({
        'message': f'File "{file.name}" uploaded successfully!',
        'url': file_url,
        'pdf_id': pdf_file.id
    })

@api_view(["GET"])
def get_pdfs(request):
    """Get all uploaded PDFs"""
    pdfs = PDFFile.objects.all().order_by('-uploaded_at')
    pdf_list = []
    for pdf in pdfs:
        pdf_list.append({
            'id': pdf.id,
            'name': pdf.name,
            'url': request.build_absolute_uri(pdf.file.url),
            'uploaded_at': pdf.uploaded_at.isoformat(),
            'annotation_count': pdf.annotations.count()
        })
    
    return JsonResponse({'pdfs': pdf_list})

@api_view(["POST"])
@parser_classes([JSONParser])
def save_annotation(request):
    """Save an annotation to the database"""
    try:
        data = request.data
        pdf_id = data.get('pdf_id')
        page_index = data.get('page_index')
        quote = data.get('quote', '')
        content = data.get('content', '')
        highlight_areas = data.get('highlight_areas', [])
        
        if pdf_id is None or page_index is None or not content:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        pdf = PDFFile.objects.get(id=pdf_id)
        annotation = Annotation.objects.create(
            pdf=pdf,
            page_index=page_index,
            quote=quote,
            content=content,
            highlight_areas=highlight_areas
        )
        
        return JsonResponse({
            'message': 'Annotation saved successfully',
            'annotation_id': annotation.id
        })
        
    except PDFFile.DoesNotExist:
        return JsonResponse({'error': 'PDF not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(["GET"])
def get_annotations(request, pdf_id):
    """Get all annotations for a specific PDF"""
    try:
        pdf = PDFFile.objects.get(id=pdf_id)
        annotations = pdf.annotations.all()
        
        annotation_list = []
        for annotation in annotations:
            annotation_list.append({
                'id': annotation.id,
                'page_index': annotation.page_index,
                'quote': annotation.quote,
                'content': annotation.content,
                'highlight_areas': annotation.highlight_areas,
                'created_at': annotation.created_at.isoformat()
            })
        
        return JsonResponse({'annotations': annotation_list})
        
    except PDFFile.DoesNotExist:
        return JsonResponse({'error': 'PDF not found'}, status=404)

@api_view(["DELETE"])
def delete_annotation(request, annotation_id):
    """Delete a specific annotation"""
    try:
        annotation = Annotation.objects.get(id=annotation_id)
        annotation.delete()
        return JsonResponse({'message': 'Annotation deleted successfully'})
    except Annotation.DoesNotExist:
        return JsonResponse({'error': 'Annotation not found'}, status=404)
