from rest_framework.permissions import BasePermission, SAFE_METHODS
from goals.models import BoardParticipant, Board


class ObjectPermissions(BasePermission):
    def get_participant(self, request, board):
        return BoardParticipant.objects.get(
                user=request.user, board=board)
    
    def has_board_editing_permissions(self, request, board):
        participant = self.get_participant(request, board)
        return participant.role in (1, 2)
    
    def is_owner(self, request, obj):
        return request.user == obj.user
                
    def has_object_permission(self, request, view, obj):
        pass


class ObjectCreatePermissions(ObjectPermissions):
    def has_object_permission(self, request, view, obj):
        return super().has_board_editing_permissions(request, view, obj)
    
    
class GoalCategoryCreatePermissions(ObjectCreatePermissions):
    def has_object_permission(self, request, view, obj):
        return super().has_board_editing_permissions(request, view, obj)
    

class GoalCreatePermissions(ObjectCreatePermissions):
    def has_object_permission(self, request, view, obj):
        return super().has_board_editing_permissions(request, view, obj.board)
    

class CommentCreatePermissions(ObjectCreatePermissions):
    def has_object_permission(self, request, view, obj):
        return super().has_board_editing_permissions(request, view, obj)
    

class GoalPermissions(ObjectPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return super().is_owner(request, obj)
        board = Board.objects.get(goalcategory=obj.category)
        participant = super().get_participant(request, board)
        return participant is not None
    
    
class GoalCategoryPermissions(ObjectPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return super().is_owner(request, obj)
        board = Board.objects.get(goalcategory=obj)
        participant = super().get_participant(request, board)
        return participant is not None


class GoalCommentPermissions(ObjectPermissions):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return super().is_owner(request, obj)
        board = Board.objects.get(goal__category=obj)
        participant = super().get_participant(request, board)
        return participant is not None
                    
    
class BoardPermissions(ObjectPermissions):  
    def has_object_permission(self, request, view, obj):
        participant = super().get_participant(request, obj)
        if request.method in SAFE_METHODS:
            return participant is not None
        return participant.role == 1