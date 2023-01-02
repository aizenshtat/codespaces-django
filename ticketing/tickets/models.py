from django.db import models

class WaitingRoom(models.Model):
    """
    A waiting room where tickets can be issued.
    """
    name = models.CharField(max_length=50)
    staff = models.ManyToManyField("Staff")

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
    status = models.CharField(max_length=50)
    counter = models.ForeignKey(Counter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ticket_id

class Staff(models.Model):
    """
    A staff employee who can manage tickets in one or more waiting rooms.
    """
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SuperUser(models.Model):
    """
    A superuser who has full access to all waiting rooms and counters.
    """
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
