from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Like, Rating, Comment, Dislike

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

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating 
    
    def validate_rating(self, rating):
        if not 0 <= rating <= 10:
            raise ValidationError(
                'Рейтинг должен быть от 0 до 10'
            )
        return rating
    

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


    class Meta:
        model = Rating
        fields = '__all__'