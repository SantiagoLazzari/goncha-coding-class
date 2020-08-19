from experta import *
from facts import *
from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import os

####### WS #######

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('init.html')

@app.route("/handle_data")
def handle_data():
    """
    age=12
    duration=short
    budget=short
    partners=12
    companion_type=partner
    distance_preference=partner
    destiny_count=partner
    excursions_preference=partner
    nature_preference=partner
    """

    age = request.args.get('age')
    duration = request.args.get('duration')
    budget = request.args.get('budget')
    partners = request.args.get('partners')
    companion_type = request.args.get('companion_type')
    distance_preference = request.args.get('distance_preference')
    destiny_count = request.args.get('destiny_count')
    excursions_preference = request.args.get('excursions_preference')
    nature_preference = request.args.get('nature_preference')

    print(f"""
    Params
        age={age}
        duration={duration}
        budget={budget}
        partners={partners}
        companion_type={companion_type}
        distance_preference={distance_preference}
        destiny_count={destiny_count}
        excursions_preference={excursions_preference}
        nature_preference={nature_preference}
    """)

    engine = TuristAgent()
    engine.reset()
    cliente_ej = InfoCliente(
        edad=age,
        duracion=duration, 
        presupuesto=budget, 
        acompanantes=int(partners), 
        tipo_acomp=companion_type, 
        pref_dist=distance_preference, 
        pref_cant_destinos=destiny_count, 
        pref_excursiones="Pocas", 
        pref_naturaleza="Mucha"
    )   
    engine.declare(cliente_ej)
    engine.run()

    if len(engine.packages) == 0:
        return render_template('zrp.html')

    new_packs = []

    for pack in engine.packages:
        new_packs.append(pack)

    return render_template('response.html', packages=new_packs)


###### ENGINNE #######

class TuristAgent(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.packages = []

    @Rule(InfoCliente(duracion="Media", 
                      presupuesto="Bajo", 
                      acompanantes=MATCH.ac & P(lambda ac: ac <= 3), 
                      tipo_acomp="Pareja", 
                      pref_dist="Mucha", 
                      pref_cant_destinos="Pocos", 
                      pref_excursiones="Pocas", 
                      pref_naturaleza="Mucha"))
    def nuevo_paquete_1(self, ac):
        dests = ["Ushuaia"]
        paquete = PaqueteViaje(nombre="Viaje a Ushuaia", duracion=3, personas=ac+1, costo=7000*ac, estadias=dests, distancia="Poca", actividades="Pocas", naturaleza="Mucha")
        self.declare(paquete)

    @Rule(InfoCliente(duracion="Poca", 
                      presupuesto="Bajo", 
                      acompanantes=MATCH.ac & P(lambda ac: ac <= 3), 
                      tipo_acomp="Pareja", 
                      pref_dist="Mucha",
                      pref_excursiones="Pocas", 
                      pref_naturaleza="Mucha"))
    def nuevo_paquete_2(self, ac):
        dests = ["Mendoza", "San Rafael", "San Juan"]
        paquete = PaqueteViaje(nombre="Bordeando de la cordillera", duracion=10, personas=ac+1, costo=12000*ac, estadias=dests, distancia="Media", actividades="Muchas", naturaleza="Mucha")
        self.declare(paquete)


    @Rule(InfoCliente(duracion="Media", 
                      presupuesto="Medio", 
                      acompanantes=MATCH.ac & P(lambda ac: ac >= 3), 
                      tipo_acomp="Amigos", 
                      pref_dist=MATCH.dist & P(lambda dist: dist == "Poca" or dist == "Media"),
                      pref_cant_destinos=MATCH.dest & P(lambda dest: dest == "Pocos" or dest == "Media")))
    def nuevo_paquete_6(self, ac):
        dests = ["Mar del Plata"]
        paquete = PaqueteViaje(nombre="Costa Argentina", duracion=10, personas=ac+1, costo=2500*ac, estadias=dests, distancia="Poca", actividades="Muchas", naturaleza="Baja")
        self.declare(paquete)

    @Rule(InfoCliente(duracion="Media", 
                      presupuesto="Alto", 
                      acompanantes=MATCH.ac & P(lambda ac: ac == 2), 
                      tipo_acomp="Pareja", 
                      pref_dist="Media",
                      pref_cant_destinos=MATCH.dest & P(lambda dest: dest == "Pocos" or dest == "Media")))
    def nuevo_paquete_3(self, ac):
        dests = ["Iguazú", "Salta"]
        paquete = PaqueteViaje(nombre="Cataratas del norte", duracion=7, personas=ac+1, costo=20000*ac, estadias=dests, distancia="Media", actividades="Muchas", naturaleza="Alta")
        self.declare(paquete)


    @Rule(PaqueteViaje(nombre=MATCH.nomb, duracion=MATCH.dur, personas=MATCH.pers, costo=MATCH.cost, estadias=MATCH.est, distancia=MATCH.dist, actividades=MATCH.act, naturaleza=MATCH.nat))
    def paquete_apropiado(self, nomb, dur, pers, cost, est, dist, act, nat):
        self.packages.append(PaqueteViaje(nombre=nomb, duracion=dur, personas=pers, costo=cost, estadias=est, distancia=dist, actividades=act, naturaleza=nat))
        print("Paquete apropiado para cliente:")
        print("\t Personas: {}".format(pers))
        print("\t Duracion: {} noches".format(dur))
        print("\t Costo total: ${}".format(cost))
        print("\t Estadias: {}".format(list(est)))
        print("\t Distancia: {}".format(dist))
        print("\t Actividades: {}".format(act))
        print("\t Naturaleza: {}".format(nat))


if __name__ == "__main__":
    app.run(debug=True)
