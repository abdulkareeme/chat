from django.db import models
from core.models import User
# Create your models here.

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    room_name = models.TextField(max_length=100)
class Message(models.Model):
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE , related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta : 
        ordering = ["-time"]
    def __str__(self):
        return self.content+' '+str(self.time)