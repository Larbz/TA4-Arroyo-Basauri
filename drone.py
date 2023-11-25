from globals import Global
import random
from pade.core.agent import Agent
from behaviours import CompRequest


class DroneAgent(Agent):
    def __init__(self, aid,id):
        super(DroneAgent, self).__init__(aid=aid, debug=False)
        self.busy = False
        self.delivery_Time = 5
        self.id = id
        self.deliveringTo = None
        self.x = random.randint(0,980)
        self.y = random.randint(0,1050)
        self.sprite = "images/dron.png"
        self.busySprite = "images/dronBusy.png"
        self.type='dron'
        self.clientId = None
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)
    def deliver(self):
        #SI EL DRON ESTA LIBRE SE PROCEDERA A DARLE EL ESTADO A OCUPADO
        if(self.busy == False):
            self.busy = True
        else:
        #SI EL DRON ESTA OCUPADO SE EJECUTARA LOS CAMBIOS DE TIEMPO DE ENVIO
            print("Entregando")
            self.delivery_Time -=2
            if(self.delivery_Time <=0):
                #SI EL TIEMPO DE ENVIO TERMINA SE REINICIAN LOS ESTADOS
                self.busy = False
                self.delivery_Time = 5
                print("Delivery completed from {} to {}".format(self.aid.localname,self.deliveringTo))
                #SE PROCEDE A ASIGNARLE ESTADO RECIBIDO A EL CLIENTE
                Global.clientList[self.clientId].get('agent').received = True
                #SE LE ELIMINA EL OBJETIVO DE ENVIO
                self.deliveringTo= None
                #SE VUELVE AGREGAR EL DRON A LA COLA
                Global.droneDeque.append(Global.droneList[self.id])

