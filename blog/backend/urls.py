from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostAPIView, CommentAPIView

router = DefaultRouter()
router.register(r'posts', PostAPIView)
router.register(r'comments', CommentAPIView)

urlpatterns = [
    path('', include(router.urls)),
]