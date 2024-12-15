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
            
    def obtener_ultimo(self):
        if self.esVacia():
            return None
        aux = self.inicio
        while aux.siguiente is not None:
            aux = aux.siguiente
        return aux.dato    
    
    #Añade los elementos de un iterable al final de la lista enlazada
    def extend(self, iterable):
        for elemento in iterable:
            nuevo_nodo = Nodo(elemento)  
            self.agregarFinal(nuevo_nodo)
    
class NodoTiempo:
    def __init__(self, titulo, cuerpo, tiempo):
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.tiempo = tiempo
        self.siguiente = None

    def __str__(self):
        return f"Título: {self.titulo}\nCuerpo: {self.cuerpo}\nÚltima edición: {self.tiempo.strftime('%Y-%m-%d %H:%M:%S')}"

class Pila:
    def __init__(self):
        self.cima = None

    def es_vacia(self):
        return self.cima is None

    def apilar(self, titulo, cuerpo, tiempo):
        nuevo_nodo = NodoTiempo(titulo, cuerpo, tiempo)
        nuevo_nodo.siguiente = self.cima
        self.cima = nuevo_nodo

    def desapilar(self):
        if self.es_vacia():
            print("La pila está vacía. No se puede desapilar.")
            return None
        nodo_eliminado = self.cima
        self.cima = self.cima.siguiente
        return nodo_eliminado

    def mostrar_titulos(self):
        if self.es_vacia():
            print("La pila está vacía.")
            return
        nodo_iter = self.cima
        indice = 0
        print("Títulos de las notas:")
        while nodo_iter:
            print(f"[{indice}] {nodo_iter.titulo} (Última edición: {nodo_iter.tiempo.strftime('%Y-%m-%d %H:%M:%S')})")
            nodo_iter = nodo_iter.siguiente
            indice += 1

    def obtener_por_indice(self, indice):
        if not isinstance(indice, int) or indice < 0:
            print("El índice debe ser un número entero no negativo.")
            return None
        nodo_iter = self.cima
        actual_indice = 0
        while nodo_iter:
            if actual_indice == indice:
                return nodo_iter
            nodo_iter = nodo_iter.siguiente
            actual_indice += 1
        print("Índice fuera de rango.")
        return None
    
    def mover_a_inicio(self, nodo_a_mover):
        if nodo_a_mover == self.cima:
            return
        nodo_iter = self.cima
        while nodo_iter and nodo_iter.siguiente != nodo_a_mover:
            nodo_iter = nodo_iter.siguiente

        if nodo_iter:
            nodo_iter.siguiente = nodo_a_mover.siguiente
            nodo_a_mover.siguiente = self.cima
            self.cima = nodo_a_mover
