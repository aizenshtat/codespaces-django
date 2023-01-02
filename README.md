# Ticketing System

This is a web-based ticketing system for physical waiting rooms. It allows users to join a waiting room queue by scanning a unique QR code, and provides a unique URL for each ticket that displays the ticket information and allows users to cancel their ticket or move back in the queue. Staff employees can view, add, and remove tickets, and move tickets back or forward in the queue. Super-users can view and edit waiting rooms and counters, and assign staff to specific rooms and counters.

## Features

- User-friendly interface for joining a waiting room queue
- Unique URL for each ticket with real-time updates on ticket status, counter, place in queue, and ticket ID
- Ability to cancel ticket or move back in queue
- Staff dashboard with options to view, add, and remove tickets, and move tickets back or forward in queue
- Super-user dashboard with options to view, create, remove, and edit waiting rooms and counters, and assign staff to specific rooms and counters
- Feedback on all actions

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Django 3.1 or higher

### Installation

1. Clone the repository:

```bash
git clone https://github.com/user/repo.git
```

2. Navigate to the project directory:

```bash
cd ticketing
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

### Accessing the App

To access the app, open your web browser and navigate to `http://127.0.0.1:8000/`. This will open the home page of the app, where you can access the different features as described in the "Usage" section.

Alternatively, you can access the staff and super-user dashboards by logging in at `http://127.0.0.1:8000/login/`.

### Usage

To use the app, follow these steps:

1. Open the app in your web browser.
2. For users:
   1. Scan the QR code for the waiting room you want to join.
   2. Access the unique URL provided for your ticket to view your ticket information and cancel your ticket or move back in the queue.
3. For staff employees:
   1. Log in with your staff credentials.
   2. Select the waiting room you want to view from the list.
   3. View, add, and remove tickets, and move tickets back or forward in the queue.
4. For super-users:
   1. Log in with your super-user credentials.
   2. View, create, remove, and edit waiting rooms and counters.
   3. Assign staff to specific rooms and counters.

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used

## Authors

- **Daniil Aizenshtat** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django team for creating a powerful and easy-to-use web framework.
- This project would not have been possible without the work of the OpenAI team, who developed the Assistant language model used to generate the code and documentation for this app.