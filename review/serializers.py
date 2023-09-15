from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Like, Rating, Comment, Dislike, Favorite
from product import serializers as ProductListSerializer

class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'


    def create(self, validated_data):
        user = self.context.get('request').user
        print('=====================')
        print(user)
        print('=====================')
        comment = Comment.objects.create(author=user, **validated_data)
        return comment



class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    
    def validate_rating(self, rating):
        if rating in range(1, 6):
            return rating
        raise ValidationError(
                'Рейтинг должен быть от 1 до 5'
            )
        

    def validate_product(self, product):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, author=user).exists():
            raise ValidationError(
                'Вы уже оставляли отзыв на данный продукт'
            )
        return product

    
    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)



class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'


    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)
    


class DislikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()


    class Meta:
        model = Dislike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)
    


class FavoriteListSerializer(ModelSerializer):
    product = ProductListSerializer

    class Meta:
        model = Favorite
        fields = ['product']


class FavoriteCreateSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = Favorite
        fields = '__all__'

