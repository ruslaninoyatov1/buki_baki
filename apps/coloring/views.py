from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Coloring

@csrf_exempt
def coloring_list(request):
    colorings_queryset = Coloring.objects.all()
    colorings = []
    for coloring in colorings_queryset:
        colorings.append({
            'id': coloring.id,
            'title': coloring.title,
            'description': coloring.description,
            'preview': coloring.preview.url if coloring.preview else None,
            'file': coloring.file.url if coloring.file else None,
            'category': {
                'id': coloring.category.id,
                'title': coloring.category.title,
                'slug': coloring.category.slug
            } if coloring.category else None,
            'created_at': coloring.created_at.isoformat()
        })
    return JsonResponse({'colorings': colorings, 'status': 'success'})

@csrf_exempt
def coloring_detail(request, coloring_id):
    coloring = get_object_or_404(Coloring, id=coloring_id)
    data = {
        'coloring': {
            'id': coloring.id,
            'title': coloring.title,
            'description': coloring.description,
            'preview': coloring.preview.url if coloring.preview else None,
            'file': coloring.file.url if coloring.file else None,
            'category': {
                'id': coloring.category.id,
                'title': coloring.category.title,
                'slug': coloring.category.slug
            } if coloring.category else None,
            'created_at': coloring.created_at.isoformat()
        },
        'status': 'success'
    }
    return JsonResponse(data)