import sys
import threading
from PySide6.QtWidgets import QApplication
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import start_loop, display_message
from pade.core.agent import Agent
from gui import Gui
from pade.behaviours.protocols import FipaRequestProtocol
from pade.acl.messages import ACLMessage
import random 
from collections import deque
class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the Time agent.
    """
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        

        if(self.agent.busy == False):
            display_message(self.agent.aid.localname, "Se envia el pedido del cliente {}".format(message.content))
            msg = eval(message.content)
            self.agent.deliveringTo = msg.get('name')
            self.agent.clientId = msg.get('id')
            self.agent.busy = True
            self.agent.deliver()

        else:
            # print("We delivering")
            self.agent.deliver()

        # print(message)
        # reply = message.create_reply()
        # reply.set_performative(ACLMessage.INFORM)
        # reply.set_content("baja")
        # self.agent.send(reply)


class CompRequest2(FipaRequestProtocol):
    """FIPA Request Behaviour of the Clock agent.
    """
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent,
                                           message=message,
                                           is_initiator=True)

    # def handle_inform(self, message):
    #     display_message(self.agent.aid.localname, message)


class ComportTemporal(TimedBehaviour):
    """Timed Behaviour of the Clock agent"""
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        # print(len(droneDeque))
        if(len(droneDeque)!=0):
            # try:
                if(self.agent.isEating == False):
                    name = droneDeque[0].get('name')
                    self.agent.createMessage(name)                
                    self.agent.changingDeliverState()
                    droneDeque.popleft()
            # except:
                # pass
        # else:
        #     print("Todos los drones estan ocupados")
        #     print(len(droneList))
        #     print(len(droneDeque))
        elif(self.agent.received == False):
            if(self.agent.deliveryName!= None):
                self.agent.createMessage(self.agent.deliveryName)    
                self.agent.changingDeliverState()          
        elif(self.agent.received == True):
            self.agent.changingDeliverState()  
        gui.update()


class DroneAgent(Agent):
    """Class that defines the Time agent."""
    def __init__(self, aid,id):
        super(DroneAgent, self).__init__(aid=aid, debug=False)
        self.busy = False
        self.comport_request = CompRequest(self)
        self.delivery_Time = 5
        self.behaviours.append(self.comport_request)
        self.id = id
        self.deliveringTo = None
        self.x = random.randint(0,980)
        self.y = random.randint(0,1050)
        self.sprite = "images/dron.png"
        self.busySprite = "images/dronBusy.png"
        self.type='dron'
        self.clientId = None
    def deliver(self):
        if(self.busy == False):
            self.busy = True
            # print("Entregando")
        else:
            print("Entregando")
            self.delivery_Time -=2
            if(self.delivery_Time <=0):
                self.busy = False
                self.delivery_Time = 5
                print("Delivery completed from {} to {}".format(self.aid.localname,self.deliveringTo))
                clientList[self.clientId].get('agent').received = True
                # print(clientList[self.clientId])
                self.deliveringTo= None
                droneDeque.append(droneList[self.id])
                # print(self.id)
                # print(type(self.id))


class ClientAgent(Agent):
    def __init__(self,aid, id):
        super(ClientAgent, self).__init__(aid=aid)
        self.x = random.randint(0,980)
        self.y = random.randint(0,1050)
        self.size = random.randint(5, 30)
        self.status = -1
        self.spriteId = random.randint(0,5)
        self.askingForDeliver = False
        self.received = False
        self.eatingTime = random.randint(5,10)
        self.isEating = False
        self.deliveryTime = None
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)
        self.message = None
        self.deliveryName = None
        self.comport_request = CompRequest2(self, self.message)
        self.name = self.aid.name
        self.type = 'client'
        # Originalmente usamos 0.2
        self.comport_temp = ComportTemporal(self, 2, self.message)
        self.sprite = 'images/character.png'
        self.eatingSprite = 'images/characterEating.png'
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)
        self.id = id
    def createMessage(self,destinateTo):
        self.deliveryName = destinateTo
        self.message = ACLMessage(ACLMessage.REQUEST)
        self.message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        self.message.add_receiver(AID(name=destinateTo))
        self.message.set_content(str({
            'name':self.name,
            'id':self.id
            }))
        self.send(self.message)



    # CORREGIR TIEMPOS DE DELIVERY TIME EN CLASES CLIENT!
 

    def changingDeliverState(self):
        if(self.isEating == False):
            if(self.received == True):
                self.isEating = True
        elif(self.isEating == True):
            self.eatingTime-=2
            if(self.eatingTime<=0):
                self.isEating = False
                self.eatingTime=random.randint(5,10)
                self.received = False
        # if(droneDeque.count != 0):
            # if(self.received == False):
            #     if(self.askingForDeliver == False):
            #         if(random.randint(0,1) == 1):
            #             self.askingForDeliver = True
            #             self.deliveryTime = random.randint(3,10)
            #             self.received=False
            #     else:
            #         if(self.deliveryTime<=0):
            #             self.askingForDeliver = False
            #             self.eatingTime = random.randint(10,20)
            #             self.received = True
            #         else:
            #             self.deliveryTime-=2
                
            # else:
            #     if(self.eatingTime<=0):
            #         self.received=False
            #     self.eatingTime-=0.2
            # print("executing")





def agentsexec():
    start_loop(agents)

if __name__ == '__main__':
    agents = list()
    droneList = list()
    droneDeque = deque()
    clientList=list()
    c=0
    # for i in range(8):
    #     port = int(sys.argv[1]) + c
    #     host_agent_name = 'host_agent_{}@localhost:{}'.format(port, port)
    #     host_agent = HostAgent(AID(name=host_agent_name),c,port)
    #     agents.append(host_agent)
    #     c += 1
    dron_id=0
    client_id=0
    for i in range(10):
        port = int(sys.argv[1]) + c
        time_agent_name = 'agent_drone_{}@localhost:{}'.format(port, port)

        # inform
        clock_agent_name = 'agent_client_{}@localhost:{}'.format(port - 10000, port - 10000)
        clock_agent = ClientAgent(AID(name=clock_agent_name),client_id)
        agents.append(clock_agent)

        clientList.append({
            'name':clock_agent_name,
            'agent':clock_agent
        })

        client_id+=1

        # inform
        clock_agent_name2 = 'agent_client_{}@localhost:{}'.format(port - 9999, port - 9999)
        clock_agent2 = ClientAgent(AID(name=clock_agent_name2),client_id)
        agents.append(clock_agent2)

        clientList.append({
            'name':clock_agent_name2,
            'agent':clock_agent2
        })


        client_id+=1


        # inform
        clock_agent_name3 = 'agent_client_{}@localhost:{}'.format(port - 9998, port - 9998)
        clock_agent3 = ClientAgent(AID(name=clock_agent_name3),client_id)
        agents.append(clock_agent3)

        clientList.append({
            'name':clock_agent_name3,
            'agent':clock_agent3
        })
        
        # request
        # time_agent_name = 'agent_drone_{}@localhost:{}'.format(port, port)
        time_agent = DroneAgent(AID(name=time_agent_name),dron_id)
        agents.append(time_agent)
        droneDeque.append({
            'name':time_agent_name,
            'agent': time_agent,
        })
        droneList.append({
            'name':time_agent_name,
            'agent': time_agent
        })

        # print(droneDeque[0].get('name'))
        c += 500
        dron_id+=1
        client_id+=1




    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    gui = Gui(agents)
    gui.show()
    app.exec()
    x.join()

