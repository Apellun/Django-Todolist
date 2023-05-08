from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.http import HttpResponse

from goals.permissions import BoardPermissions, GoalCategoryEditPermissions, GoalEditPermissions, CommentEditPermissions
from goals.models import GoalCategory, Goal, Status, GoalComment, Board, BoardParticipant, Role
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer
    
    def create(self, request, *args, **kwargs):
        participant = BoardParticipant.objects.get(board=self.request.data['board'], user=self.request.user)
        if participant is None or participant.role not in (Role.owner, Role.editor):
            return HttpResponse("You can't create goal categories in the boards you are not the owner or the editor of.")
        return super().create(request, *args, **kwargs)


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
            board__boardparticipant__user=self.request.user,
            is_deleted=False
            )

    
class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryEditPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__boardparticipant__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance): #TODO: doesn't work
        instance.is_deleted = True
        instance.save()
        for goal in Goal.objects.filter(user=self.request.user, category=instance.id):
            goal.status = Status.archived
            goal.save()
        return instance
    
#Goal views

class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer
    
    def create(self, request, *args, **kwargs):
        participant = BoardParticipant.objects.get(board__goalcategory=self.request.data['category'], user=self.request.user)
        if participant is None or participant.role not in (Role.owner, Role.editor):
            return HttpResponse("You can't create goals in the categories you are not the owner or the editor of.")
        return super().create(request, *args, **kwargs)


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
        boards = Board.objects.filter(boardparticipant__user=self.request.user)
        return Goal.objects.filter(
            category__board__in=boards,
            is_deleted=False
            )
    

class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalEditPermissions]

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipant__user=self.request.user)
        return Goal.objects.filter(
            category__board__in=boards,
            is_deleted=False
            ) #TODO: maybe add to the others

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance
    
#GoalComment views

class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer
    
    def create(self, request, *args, **kwargs): #TODO: see if it can be done better
        board = Board.objects.get(goalcategory__goal=request.data['goal'])
        participant = BoardParticipant.objects.get(board=board, user=request.user)
        
        if participant.role not in (Role.owner, Role.editor):
            return HttpResponse("You can't create comments in the goal you are not the owner or the editor of.")
        return super().create(request, *args, **kwargs)
    
    

class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipant__user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__in=boards)
    

class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentEditPermissions]

    def get_queryset(self):
        boards = Board.objects.filter(boardparticipant__user=self.request.user)
        return GoalComment.objects.filter(goal__category__board__in=boards)
    

#BoardViews

class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(boardparticipant__user=self.request.user, is_deleted=False)
        
    def perform_destroy(self, instance: Board):#TODO: check
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived
            )
        return instance
    

class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            boardparticipant__user=self.request.user,
            is_deleted=False
            )