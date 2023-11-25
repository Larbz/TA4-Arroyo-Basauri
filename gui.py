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


    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.drawPixmap(0,0,self.background)
        for host in self.agent:
            if(host.type == 'client'):
                if(host.isEating == True ):
                    #SI EL AGENTE ES DE TIPO CLIENTE Y ESTA COMIENDO SE DIBUJA SU SPRITE COMIENDO
                    sprite = QPixmap(host.eatingSprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
                else:
                    #SI EL AGENTE ES DE TIPO CLIENTE Y NO ESTA COMIENDO SE DIBUJA SU SPRITE DE LIBRE
                    sprite = QPixmap(host.sprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
            else:
                if(host.busy):
                    #SI EL AGENTE ES DE TIPO DRON Y ESTA ENVIANDO UN PEDIDO SE DIBUJA SU SPRITE OCUPADO
                    sprite = QPixmap(host.busySprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)
                else:
                    #SI EL AGENTE ES DE TIPO DRON Y ESTA LIBRE SE DIBUJA SU SPRITE LIBRE
                    sprite = QPixmap(host.sprite)
                    own_sprite = sprite.scaled(40,80)
                    painter.drawPixmap(host.x,host.y,own_sprite)


