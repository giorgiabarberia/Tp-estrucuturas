class Nodo:
    def __init__(self,dato):
        self.dato=dato
        self.siguiente=None

    def __str__(self):
        return f'{self.dato}'

class Pila:
    def __init__(self):
        self.cima=None
    
    def esVacia(self):
        return self.cima==None
    
    def apilar (self,dato):
        nuevo_nodo= Nodo (dato) 
        nuevo_nodo.siguiente = self.cima #la direccion a la que apunta el nodo apunta para abajo 
        self.cima=nuevo_nodo #ahora la cima de la pila es el nuevo nodo que agregue
    
    def desapilar(self):
        if not Pila.esVacia(self):
            nodo_eliminado=self.cima
            self.cima=self.cima.siguiente  #el progorama lo va a eliminar porque nada esta direccionado a eso
        return nodo_eliminado

    def VisualizarPila(self):
        if not Pila.esVacia(self):
            nodo_iter = self.cima
            while nodo_iter != None:
                print(nodo_iter)
                nodo_iter = nodo_iter.siguiente
        else:
            print('Pila esta vacia')


class Cola:
    def __init__(self):
        self.cola=[]  
    
    def esVacia(self):
        return self.cola==None

    def encolar(self,persona):
        self.cola.append(persona)
   
    def desencolar (self):
        if not Cola.esVacia(self):
            eliminado=self.cola.pop(0)
        return eliminado
    
    def VisualizarCola(self):
        for cola in self.cola:
            print(cola)
    
    def longitud(self):
        print(len(self.cola))