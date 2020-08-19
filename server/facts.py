from experta import Fact

class PaqueteViaje(Fact):
    """
    Informacion del paquete de viaje:
        PaqueteViaje(nombre="Pack 1", duracion=3, personas=2, costo=10000, estadias=["Lugar1", "Lugar2"], distancia="mucha", actividades="pocas", naturaleza="mucha"))
    """
    pass

class InfoCliente(Fact):
    """
    Informacion del cliente que quiere adquirir el viaje:
        InfoCliente(edad=32, duracion="Poca", presupuesto="Bajo", acompanantes=1, tipo_acomp="Pareja", pref_dist="Mucha", pref_cant_destinos="Pocos", pref_excursiones="Pocas", pref_naturaleza="Mucha")
    """
    pass