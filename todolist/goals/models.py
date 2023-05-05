from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Creation date")
    updated = models.DateTimeField(verbose_name="Last update date")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)
    

class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(verbose_name="Title", max_length=255)
    user = models.ForeignKey(User, verbose_name="Author", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Deleted", default=False)
    

class Status(models.IntegerChoices):
    to_do = 1, "To do"
    in_progress = 2, "In progress"
    done = 3, "Done"
    archived = 4, "Archived"


class Priority(models.IntegerChoices):
    low = 1, "Low"
    medium = 2, "Medium"
    high = 3, "High"
    critical = 4, "Critical"


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"


    title = models.CharField(verbose_name="Title", max_length=255)
    description = models.CharField(verbose_name="Description", max_length=255, null=True)
    priority = models.PositiveSmallIntegerField(verbose_name="Priority", choices=Priority.choices, default=Priority.medium)
    status = models.PositiveSmallIntegerField(verbose_name="Status", choices=Status.choices, default=Status.to_do)
    due_date = models.DateTimeField(verbose_name="Due date", null=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Category", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Author", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Deleted", default=False)
    

class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    text = models.CharField(verbose_name="Text", max_length=255)
    goal = models.ForeignKey(Goal, verbose_name="Goal", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Author", on_delete=models.PROTECT)