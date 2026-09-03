from django.urls import path
from .views import PlatoList, MenuList, ReservaCreate, HomeView, ReservaCreate1, DiasView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home_view'),
    path('menu/list/', MenuList.as_view(), name = 'menu_list'),
    path('plato/list/<int:menu_pk>/', PlatoList.as_view(), name = 'plato_list_por_menu'),
    path('reserva/create/', ReservaCreate.as_view(), name = 'reserva_create'),
    path('reserva/first_create/', ReservaCreate1.as_view(), name = 'reserva_create_1'),
    path('reserva/dias/disponibles/', DiasView.as_view(), name = 'dia_disponible'),
    
]
