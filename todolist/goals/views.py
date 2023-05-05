from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from datetime import datetime
import json

from goals.permissions import EntityEditPermissions
from goals.models import GoalCategory, Goal, Status, GoalComment
from core.models import User
from goals.serializers import (
    CategoryCreateSerializer, GoalCategorySerializer,
    GoalCreateSerializer, GoalSerializer,
    GoalCommentCreateSerializer, GoalCommentSerializer
)
from goals.filters import GoalDateFilter

#GoalCategory views

class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class GoalCategoryListView(ListAPIView): #TODO: isnt working
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    #TODO: what is this and how it workes
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created", "board"]
    ordering = ["title"]
    search_fields = ["title", "board"]

    def get_queryset(self):
        GoalCategory.objects.filter(
            user=self.request.user,
            is_deleted=False
            )

    
class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [EntityEditPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
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
        return Goal.objects.filter(
            user=self.request.user,
            is_deleted=False
        )
    

class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [EntityEditPermissions]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user,
            id=self.kwargs['pk'],
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


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
    

class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [EntityEditPermissions]

    def get_queryset(self):
        return GoalComment.objects.all()