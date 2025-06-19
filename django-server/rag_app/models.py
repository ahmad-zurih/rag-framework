from django.db import models

class ChatLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_query = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"[{self.timestamp}] {self.user_query[:50]}..."
