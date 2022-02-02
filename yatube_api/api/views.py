from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Follow, Group, Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюест модели Post.
    PostViewSet реализует все операции CRUD.
    Для выполнения некоторых запросов необходимо разрешение:
        <POST> - только авторизованные пользователи.
        <PUT> - только автор публикации и автор-ный пользователь.
        <PATCH> - только автор публикации и автор-ный пользователь.
        <DELETE> - только автор публикации и автор-ный пользователь.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет модели Group.
    GroupViewSet реализует только запрос <GET>.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюест модели Comment.
    CommentViewSet реализует все операции CRUD.
    Для выполнения некоторых запросов необходимо разрешение:
        <POST> - только авторизованные пользователи
        <PUT> - только автор комментария и автор-ный пользователь
        <PATCH> - только автор комментария и автор-ный пользователь
        <DELETE> - только автор комментария и автор-ный пользователь
    """
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Вьюсет модели Follow.
    FollowViewSet реализует только запросы <GET> и <POST>.
        <GET> - возвращает список подписок пользователя,
    доступно только авторизованным пользователям.
        <POST> - подписка на пользвоателя переданного в теле запроса,
    доступно только авторизованным пользователям.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
