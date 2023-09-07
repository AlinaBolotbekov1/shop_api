from rest_framework.serializers import  ModelSerializer, ValidationError
from .models import Category, Product
from review.serializers import CommentSerializer
from review.models import Comment
from django.db.models import Avg


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__' 



class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


    def validate_price(self, price):
        if price <= 0:
            raise ValidationError(
                'Стоимость не может быть 0 или меньше'
            )
        return price 
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['comments'] = CommentSerializer(Comment.objects.filter(product=instance.pk), many=True).data
        return representation