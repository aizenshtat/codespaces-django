from django.contrib import admin
from .models import WaitingRoom, Counter, Ticket

admin.site.register(WaitingRoom)
admin.site.register(Counter)
admin.site.register(Ticket)
