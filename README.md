# Ámbar — Sistema de Reservas para Restaurante

Aplicación en Django construida como pieza de portafolio para **Ataraxea**, una agencia de desarrollo web. Simula el sitio de un restaurante real — Ámbar, Cocina de Brasa — con un sistema de menú funcional y un flujo de reservas en vivo, construido enteramente con código propio en lugar de un constructor de páginas o una plantilla. El enfoque del proyecto está en el backend: modelos, lógica de disponibilidad y validaciones del lado del servidor.

> Ámbar es una marca ficticia creada con fines de demostración. No está asociada a ningún negocio real.

## Demo en vivo: https://ambarmockup.onrender.com

[Agregar aquí la URL una vez desplegada]

## Qué demuestra este proyecto

La mayoría de los sitios de negocios pequeños se construyen sobre WordPress o una plataforma similar. Este proyecto es el caso contrario: un sistema de reservas con lógica real de backend, construido desde cero en Django, para mostrar cómo se ve una solución a medida cuando un cliente necesita algo que un constructor de páginas no resuelve fácilmente — disponibilidad dinámica, verificación de capacidad y notificaciones por correo al recibir una solicitud.

## Funcionalidades

- **Sistema de menú** organizado por servicio (desayuno, almuerzo, cena), cada uno con su propio horario y platos agrupados por categoría.
- **Flujo de reserva en dos pasos**: el visitante primero elige un servicio y la cantidad de personas, y luego solo ve los horarios que realmente tienen espacio disponible para ese grupo — calculado en el momento contra las reservas existentes, no fijo de antemano.
- **Notificación automática por correo** al restaurante cuando llega una reserva nueva, usando la API de Resend.
- **Diseño responsive**, incluyendo un menú de navegación mobile hecho solo con CSS (sin JavaScript en todo el frontend).
- **Panel de administración de Django** para gestionar categorías, platos, menús y reservas sin tocar código.

## Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Django 6.1 |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Archivos estáticos | WhiteNoise |
| Correo | Resend |
| Despliegue | Render |
| Frontend | HTML5, CSS3 — sin JS, sin framework de CSS |

## Cómo funciona la lógica de reservas

Esta es la parte del proyecto de la que más orgulloso estoy, así que vale la pena explicarla brevemente:

1. El visitante elige un menú (servicio) y el número de personas. Es un formulario simple — todavía no se guarda nada.
2. El servidor calcula franjas horarias entre la hora de apertura y cierre de ese menú, y para cada franja, suma cuántas personas ya están reservadas en ella.
3. Solo las franjas que aún tienen espacio para la cantidad de personas solicitada se ofrecen como opciones válidas en el siguiente formulario.
4. La reserva final solo se guarda una vez que se selecciona una franja válida, manteniendo la verificación de capacidad del lado del servidor en vez de confiar en el frontend.

## Estructura del proyecto

```
AmbarMockup/
├── restaurante/
│   ├── models.py          # Categoria, Plato, Menu, Reserva
│   ├── views.py           # Vistas basadas en clases, flujo de reserva en dos pasos
│   ├── forms.py           # ReservaForm1 (paso 1), ReservaForm2 (paso 2, opciones dinámicas)
│   ├── utils.py           # Notificación por correo vía Resend
│   └── static/restaurante/css/
├── templates/restaurante/
├── AmbarMockup/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── manage.py
```

## Cómo correrlo en local

**Requisitos previos:** Python 3.12+, una cuenta de [Resend](https://resend.com) para las notificaciones por correo.

```bash
git clone https://github.com/MauRyze22/<nombre-del-repo>.git
cd <nombre-del-repo>

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz del proyecto:

```
SECRET_KEY=tu-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
RESEND_API_KEY=tu-api-key-de-resend
```

Luego:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Despliegue

Este proyecto está configurado para [Render](https://render.com), usando Gunicorn como servidor WSGI, WhiteNoise para los archivos estáticos, y PostgreSQL como base de datos de producción (vía `dj-database-url`). En producción, `DEBUG` se establece en `False` y `ALLOWED_HOSTS` incluye el dominio asignado por Render.

## Posibles próximos pasos

- Capacidad por mesa individual en vez de un valor de capacidad único por menú.
- Un panel para el personal donde confirmar o rechazar reservas manualmente.
- Soporte para depósitos en reservas de grupos grandes.

## Sobre este proyecto

Construido por [Amaury](https://github.com/MauRyze22) para **Ataraxea**.