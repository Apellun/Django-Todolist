from django.db import models
from core.models import User
from goals.models import Board, GoalCategory


class GoalCreatingStatus(models.IntegerChoices):
    not_initiated = 0, "Not initiated"
    start = 1, "Start"
    choosing_board = 2, "Chooding board"
    choosing_category = 3, "Choosing category"
    choosing_goal_title = 4, "Choosing goal title"
    
    
class TgUser(models.Model):
    telegram_chat_id = models.PositiveSmallIntegerField(verbose_name="Chat id")
    telegram_user_ud = models.PositiveSmallIntegerField(verbose_name="Telegram user id")
    user_id = models.ForeignKey(User, verbose_name="App user", null=True, on_delete=models.PROTECT)
    verification_code = models.PositiveSmallIntegerField(verbose_name="Verification code", null=True)
    verified = models.BooleanField(verbose_name="Verified in the app", default=False)
    goal_creating_status = models.PositiveSmallIntegerField(verbose_name="Priority", choices=GoalCreatingStatus.choices, default=0, null=True, blank=True)
    

class TgUserNewGoal(models.Model):
    board = models.ForeignKey(
        Board,
        verbose_name="Board",
        on_delete=models.CASCADE,
        null=True
    )
    
    category = models.ForeignKey(
        GoalCategory,
        verbose_name="Goal Category",
        on_delete=models.CASCADE,
        null=True
    )
    
    user = models.ForeignKey(
        TgUser,
        verbose_name="Tg User",
        on_delete=models.CASCADE
    )
