"""
URL configuration for kids_education_portal project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from . import views

# Internationalization URLs
urlpatterns = [
    path('panel/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set_language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', views.index, name='home'),
    path('videos/', include('apps.video.urls')),
    path('coloring/', include('apps.coloring.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('profile/', include('apps.profile_app.urls')),
    path('contacts/', include('apps.contacts.urls')),
    path('blog/', views.blog, name='blog'),
    path('post/', views.post, name='post'),
    path('test-translation/', views.test_translation, name='test_translation'),
    # API URLs
    path('api/', include('apps.api.urls')),
    # Mobile URLs
    path('mobile/', include('apps.api.mobile_urls')),
    # Authentication URLs (API-based)
    path('accounts/signup/', views.signup, name='signup'),
    # CKEditor URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
)

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = 'mysite.views.error_404'