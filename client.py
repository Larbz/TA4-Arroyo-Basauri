import random
from behaviours import CompRequest,ComportTemporal
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

class ClientAgent(Agent):
    def __init__(self,aid, id):
        super(ClientAgent, self).__init__(aid=aid)
        self.x = random.randint(0,980)
        self.y = random.randint(0,1050)
        #INDICA SI RECIBIO SU PEDIDO
        self.received = False
        #INDICA EL TIEMPO QUE TARDA EN COMER
        self.eatingTime = random.randint(5,10)
        #INDICA SI ESTA COMIENDO
        self.isEating = False
        self.message = None
        #INDICA EL NOMBRE DEL DRON QUE HACE EL ENVIO, SE UTILIZA PARA MAPEARLO EN LOS PROTOCOLOS FIPA
        self.deliveryName = None
        self.name = self.aid.name
        self.type = 'client'
        #SE UTILIZA PARA GUARDAR UN IDENTIFICADO QUE AYUDE A MODIFICAR SU STATUS DE RECIBIDO
        self.id = id
        self.sprite = 'images/character.png'
        self.eatingSprite = 'images/characterEating.png'
        #SE INTEGRAN LOS COMPORTAMIENTOS
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)
        self.comport_temp = ComportTemporal(self, 2, self.message)
        # self.comport_request = CompRequest2(self, self.message)
        # self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)


    #CREACION DE MENSAJES
    def createMessage(self,destinateTo):
        self.deliveryName = destinateTo
        self.message = ACLMessage(ACLMessage.REQUEST)
        self.message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        #DENTRO DE AID SE AGREGA EL NOMBRE DEL RECEIVER, SERA QUIEN RECIBIRA EL MENSAJE
        self.message.add_receiver(AID(name=destinateTo))
        #SE ENVIA INFORMACION DE NOMBRE E ID PARA MANIPULAR ESTATUS DE RECIBIDO
        self.message.set_content(str({
            'name':self.name,
            'id':self.id
            }))
        self.send(self.message)


    def changingDeliverState(self):
        #SI EL CLIENTE NO SE ENCUENTRA COMIENDO PERO RECIBIO EL PEDIDO, SE CAMBIA ESTATUS A COMIENDO
        if(self.isEating == False):
            if(self.received == True):
                self.isEating = True
        #SI EL CLIENTE ESTA COMIENDO SE REDUCIRA EN 2 SEGUNDOS EL TIEMPO DE COMIDA POR CADA EJECUCION DEL COMPORTAMIENTO
        elif(self.isEating == True):
            self.eatingTime-=2
            if(self.eatingTime<=0):
                #SI EL CLIENTE TERMINO DE COMER REINICIAMOS VARIABLES
                self.isEating = False
                self.eatingTime=random.randint(5,10)
                self.received = False
  