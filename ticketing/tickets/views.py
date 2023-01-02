from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import WaitingRoom, Counter, Ticket, Staff, SuperUser
import qrcode

def create_ticket(request, waiting_room_id):
    """
    Creates a new ticket for the given waiting room.
    """
    waiting_room = get_object_or_404(WaitingRoom, pk=waiting_room_id)
    ticket = Ticket.objects.create(
        waiting_room=waiting_room,
        unique_id=generate_unique_id(),
        place_in_queue=get_next_place_in_queue(waiting_room),
    )
    return redirect("view_ticket", ticket_id=ticket.unique_id)

def view_ticket(request, ticket_id):
    """
    Views the ticket with the given ticket ID.
    """
    ticket = get_object_or_404(Ticket, unique_id=ticket_id)
    return render(request, "tickets/view_ticket.html", {"ticket": ticket})


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

def staff_view_waiting_room(request, waiting_room_id):
    """
    Shows the staff employee a list of all tickets in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    tickets = Ticket.objects.filter(waiting_room=waiting_room)
    return render(request, "tickets/staff_view_waiting_room.html", {"tickets": tickets, "waiting_room": waiting_room})

def staff_add_ticket(request, waiting_room_id):
    """
    Adds a new ticket to the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    ticket = Ticket(waiting_room=waiting_room, ticket_id=generate_unique_id(), place_in_queue=get_next_place_in_queue(waiting_room))
    ticket.save()
    messages.success(request, "Ticket successfully added.")
    return redirect("staff_view_waiting_room", waiting_room_id=waiting_room_id)

def staff_remove_ticket(request, ticket_id):
    """
    View function for staff to remove a ticket from the queue.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('tickets:staff_view_queue')
    return render(request, 'tickets/staff_remove_ticket.html', {'ticket': ticket})

def staff_move_ticket_back(request, ticket_id):
    """
    Moves the ticket with the given ticket ID back in the queue.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.place_in_queue = move_back_in_queue(ticket)
    ticket.save()
    messages.success(request, "Ticket successfully moved back in the queue.")
    return redirect("staff_view_waiting_room", waiting_room_id=ticket.waiting_room.id)

def staff_move_ticket_forward(request, ticket_id):
    """
    Moves the ticket with the given ticket ID forward in the queue.
    """
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.place_in_queue = move_forward_in_queue(ticket)
    ticket.save()
    messages.success(request, "Ticket successfully moved forward in the queue.")
    return redirect("staff_view_waiting_room", waiting_room_id=ticket.waiting_room.id)

def staff_call_next_ticket(request, waiting_room_id, counter_id):
    """
    Calls the next ticket in the queue for the given counter in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    counter = Counter.objects.get(id=counter_id)
    next_ticket = get_next_ticket(waiting_room, counter)
    if next_ticket is not None:
        next_ticket.status = "In Service"
        next_ticket.counter = counter
        next_ticket.save()
        messages.success(request, "Ticket successfully called to counter.")
    else:
        messages.info(request, "No tickets available to be called to this counter.")
    return redirect("staff_view_waiting_room", waiting_room_id=waiting_room_id)

def superuser_view_waiting_rooms(request):
    """
    Shows the superuser a list of all waiting rooms.
    """
    waiting_rooms = WaitingRoom.objects.all()
    return render(request, "tickets/superuser_view_waiting_rooms.html", {"waiting_rooms": waiting_rooms})

def superuser_view_counters(request, waiting_room_id):
    """
    Shows the superuser a list of all counters in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    counters = Counter.objects.filter(waiting_room=waiting_room)
    return render(request, "tickets/superuser_view_counters.html", {"counters": counters, "waiting_room": waiting_room})

def superuser_create_waiting_room(request):
    """
    Creates a new waiting room.
    """
    if request.method == "POST":
        form = WaitingRoomForm(request.POST)
        if form.is_valid():
            waiting_room = form.save()
            waiting_room.save()
            messages.success(request, "Waiting room successfully created.")
            return redirect("superuser_view_waiting_rooms")
    else:
        form = WaitingRoomForm()
    return render(request, "tickets/superuser_create_waiting_room.html", {"form": form})

def superuser_remove_waiting_room(request, waiting_room_id):
    """
    Removes the waiting room with the given ID.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    waiting_room.delete()
    messages.success(request, "Waiting room successfully removed.")
    return redirect("superuser_view_waiting_rooms")

def superuser_edit_waiting_room(request, waiting_room_id):
    """
    Edits the waiting room with the given ID.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    if request.method == "POST":
        form = WaitingRoomForm(request.POST, instance=waiting_room)
        if form.is_valid():
            form.save()
            messages.success(request, "Waiting room successfully edited.")
            return redirect("superuser_view_waiting_rooms")
    else:
        form = WaitingRoomForm(instance=waiting_room)
    return render(request, "tickets/superuser_edit_waiting_room.html", {"form": form, "waiting_room": waiting_room})

def superuser_create_counter(request, waiting_room_id):
    """
    Creates a new counter in the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    if request.method == "POST":
        form = CounterForm(request.POST)
        if form.is_valid():
            counter = form.save(commit=False)
            counter.waiting_room = waiting_room
            counter.save()
            messages.success(request, "Counter successfully created.")
            return redirect("superuser_view_counters", waiting_room_id=waiting_room_id)
    else:
        form = CounterForm()
    return render(request, "tickets/superuser_create_counter.html", {"form": form, "waiting_room": waiting_room})

def superuser_remove_counter(request, counter_id):
    """
    Removes the counter with the given ID.
    """
    counter = Counter.objects.get(id=counter_id)
    waiting_room_id = counter.waiting_room.id
    counter.delete()
    messages.success(request, "Counter successfully removed.")
    return redirect("superuser_view_counters", waiting_room_id=waiting_room_id)

def superuser_edit_counter(request, counter_id):
    """
    Edits the counter with the given ID.
    """
    counter = Counter.objects.get(id=counter_id)
    if request.method == "POST":
        form = CounterForm(request.POST, instance=counter)
        if form.is_valid():
            form.save()
            messages.success(request, "Counter successfully edited.")
            return redirect("superuser_view_counters", waiting_room_id=counter.waiting_room.id)
    else:
        form = CounterForm(instance=counter)
    return render(request, "tickets/superuser_edit_counter.html", {"form": form, "counter": counter})

def superuser_assign_staff(request, waiting_room_id):
    """
    Assigns staff employees to the given waiting room.
    """
    waiting_room = WaitingRoom.objects.get(id=waiting_room_id)
    if request.method == "POST":
        form = AssignStaffForm(request.POST)
        if form.is_valid():
            staff_ids = form.cleaned_data["staff"]
            staff = Staff.objects.filter(id__in=staff_ids)
            waitingroom.staff.set(staff)
            messages.success(request, "Staff successfully assigned to waiting room.")
            return redirect("superuser_view_waiting_rooms")
    else:
        form = AssignStaffForm()
    return render(request, "tickets/superuser_assign_staff.html", {"form": form, "waiting_room": waiting_room})

def generate_unique_id():
    """
    Generates a unique ID for a ticket.
    """
    unique_id = uuid.uuid4()
    while Ticket.objects.filter(unique_id=unique_id).exists():
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
