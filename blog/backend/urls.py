from django.urls import path, include
from rest_framework_nested import routers

from .views import PostAPIView, CommentAPIView
from .cookieToken import CookieTokenRefreshView, CookieTokenObtainPairView, Logout

router = routers.DefaultRouter()
router.register(r'posts', PostAPIView)

comments_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
comments_router.register(r'comments', CommentAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', Logout.as_view()),
]
