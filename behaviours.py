from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import start_loop, display_message
from pade.behaviours.protocols import FipaRequestProtocol
from globals import Global

class CompRequest(FipaRequestProtocol):
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        #ESTA FUNCION ES EJECUTADA POR EL DRON CUANDO RECIBE UN MENSAJE
        if(self.agent.busy == False):
            #SI EL DRON ESTA LIBRE SE PUEDE RECIBIR EL PEDIDO DE ALGUN CLIENTE
            display_message(self.agent.aid.localname, "Se envia el pedido del cliente {}".format(message.content))
            msg = eval(message.content)
            self.agent.deliveringTo = msg.get('name')
            self.agent.clientId = msg.get('id')
            #ASIGNAMOS ESTADO A OCUPADO Y PROCEDEMOS A ENVIAR
            self.agent.busy = True
            self.agent.deliver()

        else:
            #SI EL CLIENTE ESTA OCUPADO SE CONTINUARA MANDANDO EL ENVIO, DEBIDO A QUE ESTE VA REDUCIENDO EL TIEMPO DE ENVIO
            self.agent.deliver()





class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        #EL CLIENTE ES QUIEN EJECUTA ESTAS FUNCIONES
        #SI AUN QUEDAN DISPONIBLES DRONES PARA ENVIO SE PROCEDE A CREAR UN NUEVO MENSAJE, Y SE QUITA DE LA COLA AL DRON QUE HARA EL ENVIO
        if(len(Global.droneDeque)!=0):
                if(self.agent.isEating == False):
                    name = Global.droneDeque[0].get('name')
                    self.agent.createMessage(name)                
                    self.agent.changingDeliverState()
                    Global.droneDeque.popleft()
        
        #SI EL CLIENTE AUN NO RECIBE SU PEDIDO, PERO YA TIENE ASIGNADO UN MOTORIZADO, SE SEGUIRAN MANDANDOS LOS MENSAJES PARA QUE SE EJECUTEN LOS ESTADOS DE ENVIO Y TAMBIEN ACTUALIZAMOS
        #SU ESTADO PROPIO DE ENVIO
        elif(self.agent.received == False):
            if(self.agent.deliveryName!= None):
                self.agent.createMessage(self.agent.deliveryName)    
                self.agent.changingDeliverState()          

        #SI EL CLIENTE YA RECIBIO SEGUIMOS ACTUALIZANDO SU ESTADO DE ENVIO
        elif(self.agent.received == True):
            self.agent.changingDeliverState()  
        Global.gui.update()