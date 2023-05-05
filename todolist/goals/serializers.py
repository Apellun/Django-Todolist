from rest_framework import serializers
from django.db import transaction

from goals.models import GoalCategory, Goal, GoalComment
from core.models import User
from core.serializers import UserSerializer

class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) #TODO: PUT IT IN THE OTHER PROJECT

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = GoalCategorySerializer

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in a deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("you are not the owner of the category")

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = GoalCategorySerializer #TODO: do that it displays the name of the category

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = GoalSerializer

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
        

    def validate_goal(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("you are not the owner of the goal")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")

    def validate_goal(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("you are not the owner of the goal")

        return value