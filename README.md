# Ámbar — Restaurant Reservation System

A full-stack Django application built as a portfolio piece for **Ataraxea**, a web development agency. It simulates a real restaurant website — Ámbar, Cocina de Brasa — with a working menu system and a live table reservation flow, built entirely with custom code rather than a page builder or template platform.

> Ámbar is a fictional brand created for demonstration purposes. No real restaurant or business is associated with this project.

## Live demo

[Add deployed URL here once available]

## What this project demonstrates

Most small-business websites are built on WordPress or a similar platform. This project is the opposite case: a reservation system with real backend logic, built from scratch in Django, to show what a custom-built solution looks like when a client needs something a page builder can't easily do — dynamic availability, capacity checks, and email notifications on submission.

## Features

- **Menu system** organized by service (breakfast, lunch, dinner), each with its own schedule and dishes grouped by category.
- **Two-step reservation flow**: the visitor first picks a service and party size, then sees only the time slots that actually have room for that many people — calculated live against existing bookings, not hardcoded.
- **Automatic email notification** to the restaurant when a new reservation comes in, using the Resend API.
- **Responsive layout**, including a CSS-only mobile navigation menu (no JavaScript anywhere in the frontend).
- **Django admin** for managing categories, dishes, menus, and reservations without touching code.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 6.1 |
| Database | SQLite (development) / PostgreSQL (production) |
| Static files | WhiteNoise |
| Email | Resend |
| Deployment | Render |
| Frontend | HTML5, CSS3 — no JS, no CSS framework |

## How the reservation logic works

This is the part of the project I'm most proud of, so it's worth explaining briefly:

1. The visitor selects a menu (service) and number of people. This is a plain form — nothing is saved yet.
2. The server calculates hourly time slots between that menu's opening and closing time, and for each slot, sums how many people are already booked in it.
3. Only slots that still have room for the requested party size are offered as valid choices in the next form.
4. The final reservation is only saved once a valid slot is selected, keeping capacity checks server-side rather than trusting the frontend.

## Project structure

```
AmbarMockup/
├── restaurante/
│   ├── models.py          # Categoria, Plato, Menu, Reserva
│   ├── views.py           # Class-based views, two-step reservation flow
│   ├── forms.py           # ReservaForm1 (step 1), ReservaForm2 (step 2, dynamic choices)
│   ├── utils.py           # Email notification via Resend
│   ├── templates/restaurante/
│   └── static/restaurante/css/
├── AmbarMockup/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── manage.py
```

## Running it locally

**Prerequisites:** Python 3.12+, a [Resend](https://resend.com) account for email notifications.

```bash
git clone https://github.com/MauRyze22/<repo-name>.git
cd <repo-name>

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
RESEND_API_KEY=your-resend-api-key
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deployment

This project is configured for [Render](https://render.com), using Gunicorn as the WSGI server, WhiteNoise for static files, and PostgreSQL as the production database (via `dj-database-url`). In production, `DEBUG` is set to `False` and `ALLOWED_HOSTS` includes the assigned Render domain.

## Possible next steps

- Per-table capacity instead of a single capacity value per menu.
- A staff-facing dashboard to confirm or reject reservations manually.
- Support for deposits on large-party bookings.

## About

Built by [Amaury](https://github.com/MauRyze22) for **Ataraxea**.