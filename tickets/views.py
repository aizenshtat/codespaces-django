from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import WaitingRoom, Counter, Ticket
import qrcode
import uuid

def home(request):
    return render(request, 'home.html')

def waiting_rooms(request):
    waiting_rooms = WaitingRoom.objects.all()
    #.filter(user__in=[request.user])
    return render(request, 'base.html', {'waiting_rooms': waiting_rooms})

def create_ticket(request, waiting_room_id):
    """
    Creates a new ticket for the given waiting room.
    """
    waiting_room = get_object_or_404(WaitingRoom, pk=waiting_room_id)
    ticket = Ticket.objects.create(
        waiting_room=waiting_room,
        ticket_id=generate_unique_id(),
        place_in_queue=get_next_place_in_queue(waiting_room),
    )
    return redirect("view_ticket", ticket_id=ticket.ticket_id)


def view_ticket(request, ticket_id):
    """
    Views the ticket with the given ticket ID.
    """
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(request, "view_ticket.html", {"ticket": ticket})


def cancel_ticket(request, ticket_id):
    """
    Cancels the ticket with the given ticket ID.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.delete()
    messages.success(request, "Ticket successfully cancelled.")
    return redirect("view_ticket", ticket_id=ticket_id)

def move_ticket(request, ticket_id):
    """
    Moves the ticket with the given ticket ID back in the queue.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.place_in_queue = move_back_in_queue(ticket)
    ticket.save()
    messages.success(request, "Ticket successfully moved back in the queue.")
    return redirect("view_ticket", ticket_id=ticket_id)

def waiting_room(request, waiting_room_id):
    """
    Shows the staff employee a list of all tickets in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    tickets = Ticket.objects.filter(waiting_room=waiting_room)
    return render(request, "waiting_room.html", {"tickets": tickets, "waiting_room": waiting_room})

def remove_ticket(request, ticket_id):
    """
    View function for staff to remove a ticket from the queue.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets:staff_view_queue')
    return render(request, 'tickets/staff_remove_ticket.html', {'ticket': ticket})

def move_ticket_back(request, ticket_id):
    """
    Moves the ticket with the given ticket ID back in the queue.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.place_in_queue = move_back_in_queue(ticket)
    ticket.save()
    messages.success(request, "Ticket successfully moved back in the queue.")
    return redirect("waiting_room", waiting_room_id=ticket.waiting_room.id)

def move_ticket_forward(request, ticket_id):
    """
    Moves the ticket with the given ticket ID forward in the queue.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.place_in_queue = move_forward_in_queue(ticket)
    ticket.save()
    messages.success(request, "Ticket successfully moved forward in the queue.")
    return redirect("waiting_room", waiting_room_id=ticket.waiting_room.id)

def call_ticket(request, waiting_room_id, counter_id):
    """
    Calls the next ticket in the queue for the given counter in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    counter = Counter.objects.get(id=counter_id)
    next_ticket = get_next_ticket(waiting_room, counter)
    if next_ticket is not None:
        next_ticket.called = True
        next_ticket.counter = counter
        next_ticket.save()
        messages.success(request, "Ticket successfully called to counter.")
    else:
        messages.info(request, "No tickets available to be called to this counter.")
    return redirect("waiting_room", waiting_room_id=waiting_room_id)

def generate_unique_id():
    """
    Generates a unique ID for a ticket.
    """
    unique_id = uuid.uuid4()
    while Ticket.objects.filter(ticket_id=unique_id).exists():
        unique_id = uuid.uuid4()
    return unique_id

def generate_qr_code(waiting_room_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(f"{request.build_absolute_uri(reverse('view_waiting_room', args=(waiting_room_id,)))}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"waiting_rooms/{waiting_room_id}.png")

def get_next_place_in_queue(waiting_room):
    """
    Gets the next available place in the queue for the given waiting room.
    """
    tickets = Ticket.objects.filter(waiting_room=waiting_room, called=False)
    places = [ticket.place_in_queue for ticket in tickets]
    next_place = 1
    while next_place in places:
        next_place += 1
    return next_place

def move_back_in_queue(ticket):
    """
    Moves the given ticket back in the queue.
    """
    ticket.called = False
    ticket.counter = None
    ticket.place_in_queue = get_next_place_in_queue(ticket.waiting_room)
    ticket.save()

def move_forward_in_queue(ticket):
    """
    Moves the given ticket forward in the queue.
    """
    ticket.called = True
    ticket.save()

def get_next_ticket(waiting_room, counter):
    """
    Gets the next ticket in the queue for the given waiting room and counter.
    """
    tickets = Ticket.objects.filter(waiting_room=waiting_room, called=False).order_by("place_in_queue")
    if not tickets:
        return None
    ticket = tickets[0]
    ticket.counter = counter
    ticket.save()
    return ticket
