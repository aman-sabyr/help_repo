from django.db import models
from account.models import User


class Message(models.Model):
    text = models.TextField()
    room = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, related_name='message', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ('created_at', )

