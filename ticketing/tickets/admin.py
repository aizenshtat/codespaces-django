from django.contrib import admin
from .models import WaitingRoom, Counter, Ticket, Staff, SuperUser

admin.site.register(WaitingRoom)
admin.site.register(Counter)
admin.site.register(Ticket)
admin.site.register(Staff)
admin.site.register(SuperUser)
