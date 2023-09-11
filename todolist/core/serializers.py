from rest_framework import serializers
from core.models import User
from goals.models import Board, BoardParticipant, Role, GoalCategory

class UserAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        board = Board.objects.create(title="My board")
        BoardParticipant.objects.create(
            user=user, board=board, role=Role.owner
        )
        GoalCategory.objects.create(title="My goals", board=board, user=user)
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    