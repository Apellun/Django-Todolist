from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from goals.permissions import (BoardPermissions, GoalCategoryCreatePermissions,
                               GoalCreatePermissions, CommentCreatePermissions,
                               GoalPermissions, GoalCategoryPermissions,
                               GoalCommentPermissions)
from goals.models import GoalCategory, Goal, Status, GoalComment, Board
from goals.serializers import (
    GoalCategoryCreateSerializer, GoalCategorySerializer,
    GoalCreateSerializer, GoalSerializer,
    GoalCommentCreateSerializer, GoalCommentSerializer,
    BoardCreateSerializer, BoardSerializer, BoardListSerializer
)
from goals.filters import GoalDateFilter

#GoalCategory views

class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, GoalCategoryCreatePermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created", "board"]
    ordering = ["title"]
    search_fields = ["title", "board"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__boardparticipants__user=self.request.user,
            is_deleted=False
            )

    
class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__boardparticipants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        for goal in Goal.objects.filter(category=instance):
            goal.status = Status.archived
            goal.save()
        return instance
    
#Goal views

class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalCreatePermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,

    ]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipants__user=self.request.user)
        return Goal.objects.filter(
            category__board__in=boards,
            is_deleted=False
            )
    

class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipants__user=self.request.user)
        return Goal.objects.filter(
            category__board__in=boards,
            is_deleted=False
            )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance
    
#GoalComment views

class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, CommentCreatePermissions]
    serializer_class = GoalCommentCreateSerializer
    
    
class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipants__user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__in=boards)
    

class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermissions]

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipants__user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__in=boards)

#BoardViews

class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(
            boardparticipants__user=self.request.user,
            is_deleted=False)
        
    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            GoalCategory.objects.filter(board=instance).update(
                is_deleted=True
            )
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived
            )
        return instance
    

class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            boardparticipants__user=self.request.user,
            is_deleted=False
            )