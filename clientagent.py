import random

from globals import Global
from pade.core.agent import Agent
from PySide6.QtGui import QColor

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




