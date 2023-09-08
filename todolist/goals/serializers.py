from rest_framework import serializers
from django.db import transaction
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant, Role
from core.models import User
from core.serializers import UserSerializer


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
    required=True, choices=Role.choices
    )#TODO: repr with words
    user = serializers.SlugRelatedField(
        slug_field="id", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        exclude = ('created', 'updated', 'is_deleted')

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=Role.owner
        )
        return board


class BoardSerializer(serializers.ModelSerializer):
    boardparticipants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"
    
    def get_user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user
        
    def update(self, instance, validated_data):
        try:
            owner = self.get_user(instance)
            new_participants = validated_data.pop("boardparticipants")
            new_participants = {participant["user"]: participant["role"] for participant in new_participants if participant["user"] != owner}
            old_boardparticipants_instances = BoardParticipant.objects.filter(board=instance)
            old_boardparticipants_roles = {boardparticipant.user: boardparticipant.role for boardparticipant in old_boardparticipants_instances if boardparticipant.user != owner}
            old_boardparticipants_instances = {boardparticipant.user: boardparticipant for boardparticipant in old_boardparticipants_instances}
            
            with transaction.atomic():
                for old_participant in old_boardparticipants_roles:
                    if old_participant not in new_participants.keys() and old_participant != owner:
                        old_boardparticipants_instances[old_participant].delete()
                    else:
                        if (
                            old_boardparticipants_roles[old_participant]
                            != new_participants[old_participant]
                        ):
                            old_boardparticipants_instances[old_participant].role = new_participants[old_participant]
                            old_boardparticipants_instances[old_participant].save()
                        del new_participants[old_participant]
                for new_participant in new_participants:
                    BoardParticipant.objects.create(
                        board=instance, user=new_participant, role=new_participants[new_participant]
                    )
        except:
            raise serializers.ValidationError("Please select participants")
        instance.title = validated_data.pop("title")
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ("id", "created", "updated")
        model = Board
        fields = "__all__"
        
        
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
            raise serializers.ValidationError("you are not the author of the comment")
        return value