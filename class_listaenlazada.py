class Nodo():
    def __init__(self,dato:int):
        self.dato = dato
        self.siguiente = None
        
    def __str__(self):
        return f'almaceno {self.dato}'

class ListaEnlazada:
    def __init__(self, inicio=None):
        self.inicio = inicio
        self.tamanio = 0  # Agregar un atributo para almacenar el tamaño
        
    def esVacia(self):
        return self.inicio==None

    def agregarInicio(self, nodo:Nodo):
        if self.esVacia():
            self.inicio = nodo
        else:
            nodo.siguiente = self.inicio
            self.inicio = nodo
        self.tamanio += 1  # Incrementar el tamaño al agregar un nodo

    def agregarFinal(self, nodo:Nodo):
        if self.esVacia():
            self.inicio = nodo
        else:
            aux = self.inicio
            while aux.siguiente is not None:
                aux = aux.siguiente
            aux.siguiente = nodo
        self.tamanio += 1  # Incrementar el tamaño al agregar un nodo

    def pop(self):
        if self.esVacia():
            return 'No se puede eliminar el primer dato'
        else:
            dato = self.inicio.dato
            self.inicio = self.inicio.siguiente
            self.tamanio -= 1  # Decrementar el tamaño al eliminar un nodo
            return f'se elimino {dato}'

    def __len__(self):  # Método para obtener la longitud de la lista
        return self.tamanio

    def __iter__(self):
        aux = self.inicio
        while aux is not None:
            yield aux.dato
            aux = aux.siguiente