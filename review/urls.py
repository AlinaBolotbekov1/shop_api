from django.urls import path, include
from .views import CommentView, RatingView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comments', CommentView)
router.register('rating', RatingView)

urlpatterns = [
    path('', include(router.urls))
]