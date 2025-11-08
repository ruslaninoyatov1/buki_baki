from django.urls import path
from . import mobile_views

app_name = 'mobile'

urlpatterns = [
    path('', mobile_views.mobile_home, name='home'),
    path('login/', mobile_views.mobile_login, name='login'),
    path('register/', mobile_views.mobile_register, name='register'),
    path('logout/', mobile_views.mobile_logout, name='logout'),
    path('categories/', mobile_views.mobile_categories, name='categories'),
    path('categories/<slug:slug>/', mobile_views.mobile_category_detail, name='category_detail'),
    path('videos/', mobile_views.mobile_videos, name='videos'),
    path('videos/<int:video_id>/', mobile_views.mobile_video_detail, name='video_detail'),
    path('colorings/', mobile_views.mobile_colorings, name='colorings'),
    path('tasks/', mobile_views.mobile_tasks, name='tasks'),
    path('profile/', mobile_views.mobile_profile, name='profile'),
    path('subscription/', mobile_views.mobile_subscription, name='subscription'),
]

