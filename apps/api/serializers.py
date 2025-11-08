from rest_framework import serializers
from apps.video.models import Video, VideoSeries
from apps.coloring.models import Coloring
from apps.tasks.models import Task
from apps.categories.models import Category
from apps.banners.models import Banner
from apps.ads.models import AdBlock
from apps.subscription.models import Subscription
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'is_free', 'description']

class VideoSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSeries
        fields = ['id', 'name', 'created_at']

class VideoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    series_group = VideoSeriesSerializer(read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'preview', 'file', 'category', 
                  'is_series', 'series_group', 'order', 'date']

class ColoringSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Coloring
        fields = ['id', 'title', 'description', 'preview', 'file', 'category', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'preview', 'file', 'difficulty', 
                  'age_group', 'category', 'created_at']

class BannerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Banner
        fields = ['id', 'title', 'description', 'image', 'category', 'external_link', 
                  'is_active', 'order', 'created_at']

class AdBlockSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    video = VideoSerializer(read_only=True)
    
    class Meta:
        model = AdBlock
        fields = ['id', 'title', 'description', 'background_image', 'content_type', 
                  'video', 'category', 'is_active', 'order', 'created_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'payment_platform', 'start_date', 'end_date', 
                  'is_active', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']