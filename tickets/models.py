from django.db import models
from django.contrib.auth.models import User

class WaitingRoom(models.Model):
    """
    A waiting room where tickets can be issued.
    """
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Counter(models.Model):
    """
    A counter in a waiting room where tickets can be serviced.
    """
    waiting_room = models.ForeignKey(WaitingRoom, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.waiting_room.name} - {self.name}"

class Ticket(models.Model):
    """
    A ticket issued in a waiting room.
    """
    waiting_room = models.ForeignKey(WaitingRoom, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=50, unique=True)
    place_in_queue = models.PositiveIntegerField()
    called = models.BooleanField(default=False)
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ticket_id