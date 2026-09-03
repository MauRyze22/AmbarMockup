from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Menu, Reserva, Plato
from .forms import ReservaForm1, ReservaForm2
from django.urls import reverse_lazy
from django.contrib import messages
from .utils import enviar_correo_reserva
from datetime import date

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'restaurante/home.html'


class MenuList(generic.ListView):
    model = Menu
    template_name = 'restaurante/menu_view.html'


class PlatoList(generic.ListView):
    model = Plato
    template_name = 'restaurante/plato_list_por_menu.html'

    def get_queryset(self):
        return Plato.objects.filter(menus__pk = self.kwargs['menu_pk'])


class ReservaCreate1(generic.FormView):
    template_name = 'restaurante/reserva_create_1.html'
    form_class = ReservaForm1

    def get(self, request, *args, **kwargs):
        if request.GET.get('menu') and request.GET.get('numero_de_personas'):
            form = self.form_class(data=request.GET)
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)
        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        self.menu_id = form.cleaned_data['menu'].id
        self.numero_de_personas = form.cleaned_data['numero_de_personas']
        return super().form_valid(form)

    def get_success_url(self):
        base_url = reverse_lazy('dia_disponible')
        return f"{base_url}?menu={self.menu_id}&numero_de_personas={self.numero_de_personas}"
        
    
class ReservaCreate(generic.CreateView):
    model = Reserva
    form_class = ReservaForm2
    template_name = 'restaurante/reserva_create.html'

    def convercion_a_date(self):
        dia_string = self.request.GET.get('dia')
        dia = date.fromisoformat(dia_string)

        return dia

    def obtener_horarios(self):
        menu_id = self.request.GET.get('menu')
        numero_personas = self.request.GET.get('numero_de_personas')
        menu = get_object_or_404(Menu, id = menu_id)

        return menu.horarios_disponibles(numero_personas, self.convercion_a_date())

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.horarios_disponibles = self.obtener_horarios()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['horarios_disponibles'] = self.horarios_disponibles

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['horarios'] = self.horarios_disponibles
        kwargs['initial'] = {
            'menu': self.request.GET.get('menu'),
            'numero_de_personas': self.request.GET.get('numero_de_personas'),
            'fecha_reserva': self.convercion_a_date()
        }
        return kwargs

        
    def form_valid(self, form):
        reserva_form = super().form_valid(form)
        enviar_correo_reserva(form.instance)
        messages.success(self.request, "Su reserva ha sido registrada correctamente, espere su respuesta")
        return reserva_form
    
    def get_success_url(self):
        return reverse_lazy('home_view')


class DiasView(generic.TemplateView):
    template_name = 'restaurante/dias_disponibles.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        menu_id = self.request.GET.get('menu')
        numero_de_personas = self.request.GET.get('numero_de_personas')
        menu = get_object_or_404(Menu, id = menu_id)

        context['fechas_disponibles'] = menu.fechas_disponibles(numero_de_personas)
        context['menu'] = menu_id
        context['numero_de_personas'] = numero_de_personas

        return context

