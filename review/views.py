from .models import Dislike, Rating, Comment
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import CommentSerializer, RatingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorOrReadOnly

class PermissionMixin:
    def get_permissions(self):
        if self.action =='create':
            permissions = [IsAuthenticated]

        elif self.action in ('update', 'partial_update', 'destroy', 'create'):
            permissions = [IsAuthorOrReadOnly]

        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CommentView(PermissionMixin,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class RatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



# class LikeView(APIView):
#     def post(self, request):
#         serializer = LikeSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Успешно', status=200)



