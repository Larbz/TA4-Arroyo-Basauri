from collections import deque
class Global:
    #Creamos un arreglo que contiene todos los agentes
    #Creamos un arreglo unicamente para clientes
    #Creamos un arreglo para drones y ademas una cola que ayudara para la asignacion de dron de delivery
    agents = list()
    droneList = list()
    droneDeque = deque()
    clientList=list()
    gui = None