from django.db import models
from datetime import timedelta, datetime, date
from django.db.models import Sum

# Create your models here

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f'categoria: {self.nombre}'

class Plato(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    descripcion = models.TextField()
    image = models.ImageField(upload_to='platos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=4, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null = True, blank = True, related_name='platos')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'Plato: {self.nombre}'


class Menu(models.Model):
    TIPO_CHOICE = [
        ('desayuno', 'Desayuno'),
        ('almuerzo', 'Almuerzo'),
        ('cena', 'Cena')
    ]

    servicio = models.CharField(max_length=20, choices=TIPO_CHOICE)
    platos = models.ManyToManyField(Plato, related_name='menus')
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    disponible = models.BooleanField(default=True)
    capacidad_maxima = models.IntegerField(default=40)

    def __str__(self):
        return f'Menu de {self.servicio}'

    def horarios_disponibles(self, personas_de_reserva):
        inicio_d = datetime.combine(date.today(), self.horario_inicio)
        tiempo_fin = datetime.combine(date.today(), self.horario_fin)
        horarios = []

        while inicio_d < tiempo_fin:

            franja_inicio = inicio_d
            franja_final = inicio_d + timedelta(hours=1)

            capacidad_total_actual = self.reservas.filter(
                hora_reserva__gte = franja_inicio,
                hora_reserva__lt = franja_final
            ).aggregate(total=Sum('numero_de_personas', default=0))

            horarios.append({'hora_inicio': franja_inicio.time(),
                                'hora_final': franja_final.time(),
                                'disponible': self.capacidad_maxima >= capacidad_total_actual['total'] + personas_de_reserva}
            )

            inicio_d += timedelta(hours=1)
            
        return horarios
    

class Reserva(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    numero_cliente = models.CharField(max_length=15)
    numero_de_personas = models.PositiveSmallIntegerField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name = 'reservas')
    hora_reserva = models.TimeField()

    def __str__(self):
        return f'Reserva de {self.nombre_cliente}'