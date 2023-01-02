from django.urls import path
from . import views

urlpatterns = [
    path("create/<str:waiting_room_qr_code>/", views.create_ticket, name="create_ticket"),
    path("view/<str:ticket_id>/", views.view_ticket, name="view_ticket"),
    path("cancel/<str:ticket_id>/", views.cancel_ticket, name="cancel_ticket"),
    path("move/<str:ticket_id>/", views.move_ticket, name="move_ticket"),
]
