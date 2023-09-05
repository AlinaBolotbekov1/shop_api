from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, ProductView

router = DefaultRouter()
router.register('categories', CategoryView)
router.register('products', ProductView)


urlpatterns = [
    path('', include(router.urls))
    # path('categories/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    # path('categories/<slug:pk>/', CategoryView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update','delete': 'destroy'}))
]