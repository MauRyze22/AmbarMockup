from django.contrib import admin
from .models import Categoria, Plato, Menu, Reserva

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Plato)
admin.site.register(Menu)
admin.site.register(Reserva)
