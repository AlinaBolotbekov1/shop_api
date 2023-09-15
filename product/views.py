from rest_framework import viewsets, filters, generics
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductListSerializer, ProductImageSerializer, ProductDetailSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from review.serializers import LikeSerializer, DislikeSerializer
from review.models import Like, Dislike
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page




class PermissionMixin:
    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy', 'create'):
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]



class CategoryView(PermissionMixin,viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(PermissionMixin,viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'in_stock']
    search_fields = ['title', 'price']

    @method_decorator(cache_page(60*5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60*2))
    def retrieve(self,request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        else:
            return self.serializer_class


    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(product=product, author=user)
                like.delete()
                message = 'Unliked'
            except Like.DoesNotExist:
                Like.objects.create(product=product, author=user)
                message = 'Liked'
            return Response(message, status=200)
        

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        product = self.get_object()
        user = request.user
        serializer = DislikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                dislike = Dislike.objects.get(product=product, author=user)
                dislike.delete()
                message = 'dislike removed'
            except Dislike.DoesNotExist:
                Dislike.objects.create(product=product, author=user)
                message = 'disliked'
            return Response(message, status=200)
        

    # @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    # def favorite(self, request, pk=None):
    #     product = self.get_object()
    #     user = request.user
    #     serializer = FavoriteSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         try:
    #             favorite = Favorite.objects.get(product=product, author=user)
    #             favorite.delete()
    #             message = 'removed from favorites'
    #         except Favorite.DoesNotExist:
    #             Favorite.objects.create(product=product, author=user)
    #             message = 'added to favorites'
    #         return Response(message, status=200)

    

class ProductImageView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer 
    permission_classes = [IsAdminUser] 









