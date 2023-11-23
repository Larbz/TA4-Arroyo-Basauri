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

    def __init__(self, aid,c):
        super(HostAgent, 
              self).__init__(aid=aid, debug=False)
        Global.x_center = 0
        self.client = ClientAgent(AID(name=aid.name),self.houses_coordenates[c])
        print(c)

        mytimed = MyTimedBehaviour(self, .2)
        yourtimed = YourTimedBehaviour(self, 2)
        self.behaviours.append(mytimed)
        self.behaviours.append(yourtimed)



def agentsexec():
    start_loop(agents)

if __name__ == '__main__':
    agents = list()

    c=0
    for i in range(8):
        port = int(sys.argv[1]) + c
        host_agent_name = 'host_agent_{}@localhost:{}'.format(port, port)
        host_agent = HostAgent(AID(name=host_agent_name),c)
        agents.append(host_agent)
        c += 1

    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    gui = Gui(agents)
    gui.show()
    app.exec()
    x.join()

