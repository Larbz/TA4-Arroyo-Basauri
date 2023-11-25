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
from globals import Global
from drone import DroneAgent
from client import ClientAgent

def agentsexec():
    start_loop(Global.agents)

if __name__ == '__main__':

    #variables para modificar id's y puertos
    c=0
    dron_id=0
    client_id=0
    
    for i in range(10):
        port = int(sys.argv[1]) + c
        time_agent_name = 'agent_drone_{}@localhost:{}'.format(port, port)

        # inform
        clock_agent_name = 'agent_client_{}@localhost:{}'.format(port - 10000, port - 10000)
        clock_agent = ClientAgent(AID(name=clock_agent_name),client_id)
        Global.agents.append(clock_agent)

        Global.clientList.append({
            'name':clock_agent_name,
            'agent':clock_agent
        })

        client_id+=1

        # inform
        clock_agent_name2 = 'agent_client_{}@localhost:{}'.format(port - 9999, port - 9999)
        clock_agent2 = ClientAgent(AID(name=clock_agent_name2),client_id)
        Global.agents.append(clock_agent2)

        Global.clientList.append({
            'name':clock_agent_name2,
            'agent':clock_agent2
        })


        client_id+=1


        # inform
        clock_agent_name3 = 'agent_client_{}@localhost:{}'.format(port - 9998, port - 9998)
        clock_agent3 = ClientAgent(AID(name=clock_agent_name3),client_id)
        Global.agents.append(clock_agent3)

        Global.clientList.append({
            'name':clock_agent_name3,
            'agent':clock_agent3
        })
        
        # request
        time_agent = DroneAgent(AID(name=time_agent_name),dron_id)
        Global.agents.append(time_agent)
        Global.droneDeque.append({
            'name':time_agent_name,
            'agent': time_agent,
        })
        Global.droneList.append({
            'name':time_agent_name,
            'agent': time_agent
        })

        c += 500
        dron_id+=1
        client_id+=1




    x = threading.Thread(target=agentsexec)
    x.start()
    app = QApplication([])
    Global.gui = Gui(Global.agents)
    Global.gui.show()
    app.exec()
    x.join()

