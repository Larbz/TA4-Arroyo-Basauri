from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPaintEvent, QPainter, QPixmap
from PySide6.QtWidgets import QFrame, QLabel


class Gui(QFrame):
    def __init__(self, agent) -> None:
        super(Gui, self).__init__()
        self.agent = agent
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.background = QPixmap("images/background.png")
        self.setFixedSize(self.background.width(), self.background.height())
        print(self.background.width(),self.background.height())
        # self.setFixedSize(1200, 1080)


    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.background)
        for host in self.agent:
            if(host.type == 'client'):
                if(host.isEating == True ):

                    sprite = QPixmap(host.eatingSprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
                else:
                    sprite = QPixmap(host.sprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
            else:
                if(host.busy):
                    sprite = QPixmap(host.busySprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
                else:
                    sprite = QPixmap(host.sprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
            # client=host.client
            # print(client.askingForDeliver)
            # own_sprite = self.sprites[client.spriteId].scaled(client.size,client.size//2)
            #    print(client.x, client.y)
            # if(client.askingForDeliver):
                # painter.fillRect(client.x-10,client.y-20,120,30,"#abb2bf")
                # painter.drawText(client.x-10,client.y,"Necesito un pedido")
            # elif(client.eatingTime>0):
                # painter.fillRect(client.x-10,client.y-20,120,30,"#abb2bf")
                # painter.drawText(client.x-10,client.y,"Estoy comiendo!")

