from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('waiting_room/<int:waiting_room_id>/', views.waiting_room, name='waiting_room'),
    path("create/<str:waiting_room_id>/", views.create_ticket, name="create_ticket"),
    path("view/<str:ticket_id>/", views.view_ticket, name="view_ticket"),
    path("cancel/<str:ticket_id>/", views.cancel_ticket, name="cancel_ticket"),
    path("move/<str:ticket_id>/", views.move_ticket, name="move_ticket"),
    path('remove/<str:ticket_id>/', views.remove_ticket, name='remove_ticket'),
    path('move/back/<str:ticket_id>/', views.move_ticket_back, name='move_ticket_back'),
    path('move/forward/<str:ticket_id>/', views.move_ticket_forward, name='move_ticket_forward'),
    path('call/<str:waiting_room_id>/<str:counter_id>/', views.call_ticket, name='call_ticket'),
]
