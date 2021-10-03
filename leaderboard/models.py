from django.db import models
import uuid


class Run(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"Run by '{self.username}' (score: {self.score})"
