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
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        exclude = ('created', 'updated')

    def create(self, validated_data): #TODO: use for the other project?
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=Role.owner
        )
        return board
    

class BoardCreateSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    boardparticipant = BoardParticipantSerializer(many=True) #TODO now it accepts boardparticipant, not participants
    # user = serializers.SlugRelatedField(
    #         slug_field="username", queryset=User.objects.all()
    #     ) #TODO: doesn't work
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
        
        if "participants" in validated_data:
            owner = self.get_user(instance)
            new_participants = validated_data.pop("participants")
            new_by_id = {participant["user"].id: participant for participant in new_participants if participant["user"].id != owner.id}

            old_participants = instance.boardparticipant.exclude(user=owner)
            #old_participants = BoardParticipant.objects.filter(board=instance).exclude(user=owner)

            with transaction.atomic():
                for old_participant in old_participants:
                    if old_participant.user_id not in new_by_id:
                        old_participant.delete()
                    else:
                        if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                        ):
                            old_participant.role = new_by_id[old_participant.user_id][
                                "role"
                            ]
                            old_participant.save()
                        new_by_id.pop(old_participant.user_id)

                for new_participant in new_by_id.values():
                    BoardParticipant.objects.create(
                        board=instance, user=new_participant["user"], role=new_participant["role"]
                    )

        if "title" in validated_data:
            instance.title = validated_data["title"]
        
        instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ("id", "created", "updated")
        model = Board
        fields = "__all__"
        
        
class GoalCategoryCreateSerializer(serializers.ModelSerializer):
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

        # participant = BoardParticipant.objects.get(board__goalcategory=self.context["request"].data['category'], user=self.context["request"].user)
        
        # if participant.role not in (1, 2):
        #     raise serializers.ValidationError("You can't perform this action")#TODO: delete or...

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