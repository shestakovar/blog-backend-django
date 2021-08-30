from django.urls import path, include
from rest_framework_nested import routers

from .views import PostAPIView, CommentAPIView

router = routers.DefaultRouter()
router.register(r'posts', PostAPIView)

comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
comments_router.register(r'comments', CommentAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls))
]
