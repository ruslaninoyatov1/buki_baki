from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Video

@csrf_exempt
def video_list(request):
    videos_queryset = Video.objects.all()
    videos = []
    for video in videos_queryset:
        videos.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': video.preview.url if video.preview else None,
            'file': video.file.url if video.file else None,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            } if video.category else None,
            'date': video.date.isoformat()
        })
    return JsonResponse({'videos': videos, 'status': 'success'})

@csrf_exempt
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    data = {
        'video': {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'preview': video.preview.url if video.preview else None,
            'file': video.file.url if video.file else None,
            'category': {
                'id': video.category.id,
                'title': video.category.title,
                'slug': video.category.slug
            } if video.category else None,
            'date': video.date.isoformat()
        },
        'status': 'success'
    }
    return JsonResponse(data)