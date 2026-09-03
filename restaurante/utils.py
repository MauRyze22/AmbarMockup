import resend 
from decouple import config

resend.api_key = config('RESEND_API_KEY')

def enviar_correo_reserva(reserva):
    resend.Emails.send({
        "from": "AmbarMockup <onboarding@resend.dev>",
        "to": "amaurymperez22@gmail.com",
        "subject": f"Nueva reserva recibida de {reserva.nombre_cliente}",
        "html": f"""
            <h2>Nuevo Pedido</h2>
            <p><strong>Cliente: {reserva.nombre_cliente}</strong></p>
            <p><strong>Numero del cliente: {reserva.numero_cliente}</strong></p>
            <p><strong>Personas incluidas en la reserva: {reserva.numero_de_personas}</strong></p>
            <p><strong>Menu: {reserva.menu}</strong></p>
            <p><strong>Horario de la reserva: {reserva.hora_reserva}</strong></p>
            <p><strong>Fecha de la reserva: {reserva.fecha_reserva}</strong></p>
        """
    })