from .models import Reserva
from django import forms
from .models import Menu

class ReservaForm2(forms.ModelForm):
    def __init__(self, *args, horarios=None, **kwargs):
        super().__init__(*args, **kwargs)
        if horarios:
            opciones = [(h['hora_inicio'], f"{h['hora_inicio']} - {h['hora_final']}") for h in horarios if h['disponible']]
            self.fields['hora_reserva'] = forms.ChoiceField(choices=opciones)

    class Meta:
        model = Reserva
        fields = ['nombre_cliente', 'numero_cliente', 'hora_reserva', 'menu', 'numero_de_personas', 'fecha_reserva']
        widgets = {
            'menu': forms.HiddenInput(),
            'numero_de_personas': forms.HiddenInput(),
            'fecha_reserva': forms.HiddenInput()
        }

class ReservaForm1(forms.Form):
    menu = forms.ModelChoiceField(queryset=Menu.objects.all(), required=True)
    numero_de_personas = forms.IntegerField(required=True)