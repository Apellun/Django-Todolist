from rest_framework.permissions import BasePermission, SAFE_METHODS

from goals.models import BoardParticipant, Role, Board, GoalCategory


class GoalCategoryEditPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.method == "DELETE":
            if obj.user != request.user:
                    return False
            
        if request.method not in SAFE_METHODS:
            board = Board.objects.get(goalcategory=obj)
            participant = BoardParticipant.objects.get(board=board, user=request.user)
            if participant.role not in (1, 2):
                return False
        
        
        return True
    

class CommentEditPermissions(BasePermission): #TODO
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.method not in SAFE_METHODS:
            if request.user != obj.user:
                return False
        
        return True
    

class GoalEditPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.method not in SAFE_METHODS:
            board = Board.objects.get(goalcategory__goal=obj)
            participant = BoardParticipant.objects.get(board=board.id, user=request.user)
    
            if participant.role in (1, 2):
                return True
            return False
        
        return True
    

class CategoryCreatePermission(BasePermission):#TODO
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        participant = BoardParticipant.objects.filter(board=request.board, user=request.user)
        
        if participant.role in (1, 2):
            return True
        return False
                    
    
class BoardPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=Role.owner
        ).exists()