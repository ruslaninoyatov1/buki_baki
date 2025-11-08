from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Task

@csrf_exempt
def task_list(request):
    tasks_queryset = Task.objects.all()
    tasks = []
    for task in tasks_queryset:
        tasks.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'preview': task.preview.url if task.preview else None,
            'file': task.file.url if task.file else None,
            'difficulty': task.difficulty,
            'age_group': task.age_group,
            'category': {
                'id': task.category.id,
                'title': task.category.title,
                'slug': task.category.slug
            } if task.category else None,
            'created_at': task.created_at.isoformat()
        })
    return JsonResponse({'tasks': tasks, 'status': 'success'})

@csrf_exempt
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    data = {
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'preview': task.preview.url if task.preview else None,
            'file': task.file.url if task.file else None,
            'difficulty': task.difficulty,
            'age_group': task.age_group,
            'category': {
                'id': task.category.id,
                'title': task.category.title,
                'slug': task.category.slug
            } if task.category else None,
            'created_at': task.created_at.isoformat()
        },
        'status': 'success'
    }
    return JsonResponse(data)