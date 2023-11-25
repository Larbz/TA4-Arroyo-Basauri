import sys
import threading
from PySide6.QtWidgets import QApplication
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import start_loop, display_message
from clientagent import ClientAgent
from pade.core.agent import Agent
import time
from globals import Global
from gui import Gui
from datetime import datetime
from pade.behaviours.protocols import FipaRequestProtocol
from pade.acl.messages import ACLMessage
import random 
from PySide6.QtGui import QColor

class CompRequest(FipaRequestProtocol):
    """FIPA Request Behaviour of the Time agent.
    """
    def __init__(self, agent):
        super(CompRequest, self).__init__(agent=agent,
                                          message=None,
                                          is_initiator=False)

    def handle_request(self, message):
        super(CompRequest, self).handle_request(message)
        display_message(self.agent.aid.localname, 'request message received')
        now = datetime.now()
        reply = message.create_reply()
        reply.set_performative(ACLMessage.INFORM)
        reply.set_content(now.strftime('%d/%m/%Y - %H:%M:%S'))
        self.agent.send(reply)


class CompRequest2(FipaRequestProtocol):
    """FIPA Request Behaviour of the Clock agent.
    """
    def __init__(self, agent, message):
        super(CompRequest2, self).__init__(agent=agent,
                                           message=message,
                                           is_initiator=True)

    def handle_inform(self, message):
        display_message(self.agent.aid.localname, message.content)


class ComportTemporal(TimedBehaviour):
    """Timed Behaviour of the Clock agent"""
    def __init__(self, agent, time, message):
        super(ComportTemporal, self).__init__(agent, time)
        self.message = message

    def on_time(self):
        super(ComportTemporal, self).on_time()
        self.agent.send(self.message)

class TimeAgent(Agent):
    """Class that defines the Time agent."""
    def __init__(self, aid):
        super(TimeAgent, self).__init__(aid=aid, debug=False)

        self.comport_request = CompRequest(self)

        self.behaviours.append(self.comport_request)


class ClockAgent(Agent):
    """Class thet defines the Clock agent."""
    def __init__(self, aid, time_agent_name):
        super(ClockAgent, self).__init__(aid=aid)

        # message that requests time of Time agent.
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name=time_agent_name))
        message.set_content('time')

        self.comport_request = CompRequest2(self, message)
        self.comport_temp = ComportTemporal(self, .2, message)
        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)


class MyTimedBehaviour(TimedBehaviour):
    def __init__(self, agent, time):
        super(MyTimedBehaviour, self).__init__(agent, time)
        self.agent = agent

    def on_time(self):
        super(MyTimedBehaviour, self).on_time()
  
        self.agent.client.changingDeliverState()

        

        gui.update()

class YourTimedBehaviour(TimedBehaviour):
    def __init__(self, agent, time):
        super(YourTimedBehaviour, self).__init__(agent, time)
        self.agent=agent


    def on_time(self):
        super(YourTimedBehaviour, self).on_time()
        Global.x_center += 3

class ClientAgent(Agent):
    def __init__(self,aid,coords):
        super(ClientAgent, self).__init__(aid=aid, debug=False)
        self.x = coords[0]
        self.y = coords[1]
        self.color = QColor(random.randint(0, 0xffffff))
        self.size = random.randint(5, 30)
        self.speed = 10 * 25 / self.size
        self.status = -1
        self.spriteId = random.randint(0,5)
        self.askingForDeliver = False
        self.received = False
        self.eatingTime = None
        self.deliveryTime = None
        self.comport_request = CompRequest(self)
        self.behaviours.append(self.comport_request)




 

    def changingDeliverState(self):
        if(self.received == False):
            if(self.askingForDeliver == False):
                if(random.randint(0,1) == 1):
                    self.askingForDeliver = True
                    self.deliveryTime = random.randint(3,10)
                    self.received=False
            else:
                if(self.deliveryTime<=0):
                    self.askingForDeliver = False
                    self.eatingTime = random.randint(10,20)
                    self.received = True
                else:
                    self.deliveryTime-=0.2
            
        else:
            if(self.eatingTime<=0):
                self.received=False
            self.eatingTime-=0.2





class HostAgent(Agent):
    gui = None
    client=None
    houses_coordenates = [
        [400,80],
        [530,90],
        [190,380],
        [58,530],
        [130,670],
        [490,700],
        [410,480],
        [1150,910]
    ]
    
    enabled = False

    def __init__(self, aid,c,port):
        super(HostAgent, 
              self).__init__(aid=aid, debug=False)
        Global.x_center = 0
        client_agent_name = 'client_agent_{}@localhost:{}'.format(port-10000, port-10000)
        self.client = ClientAgent(AID(name=client_agent_name),self.houses_coordenates[c])
        mytimed = MyTimedBehaviour(self, .2)
        yourtimed = YourTimedBehaviour(self, 2)
        self.behaviours.append(mytimed)
        self.behaviours.append(yourtimed)
        print(client_agent_name)
        message = ACLMessage(ACLMessage.REQUEST)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(AID(name=client_agent_name))
        message.set_content('time')

        self.comport_request = CompRequest2(self, message)
        self.comport_temp = ComportTemporal(self, 0.2, message)

        self.behaviours.append(self.comport_request)
        self.behaviours.append(self.comport_temp)



def agentsexec():
    start_loop(agents)

if __name__ == '__main__':
    agents = list()

    c=0
    for i in range(8):
        port = int(sys.argv[1]) + c
        host_agent_name = 'host_agent_{}@localhost:{}'.format(port, port)
        host_agent = HostAgent(AID(name=host_agent_name),c,port)
        agents.append(host_agent)
        c += 1

    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    gui = Gui(agents)
    gui.show()
    app.exec()
    x.join()

