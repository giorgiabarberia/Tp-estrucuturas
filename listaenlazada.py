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
    
class NodoTiempo():
    def __init__(self, nota, tiempo):
        self.nota = nota
        self.tiempo = tiempo
        self.siguiente = None

    def actualizar_nota(self, nueva_nota, nuevo_tiempo):
        self.nota = nueva_nota
        self.tiempo = nuevo_tiempo

    def __str__(self):
        return f"{self.nota} (Última edición: {self.tiempo.strftime('%Y-%m-%d %H:%M:%S')})"
    
class Pila:
    def __init__(self):
        self.cima = None

    def es_vacia(self):
        return self.cima is None

    def apilar(self, nota, tiempo):
        nuevo_nodo = NodoTiempo(nota, tiempo)
        nuevo_nodo.siguiente = self.cima  # El nuevo nodo apunta al nodo anterior
        self.cima = nuevo_nodo  # Ahora la cima es el nuevo nodo

    def desapilar(self):
        if self.es_vacia():
            print("La pila está vacía. No se puede desapilar.")
            return None
        nodo_eliminado = self.cima
        self.cima = self.cima.siguiente  # Actualiza la cima al siguiente nodo
        return nodo_eliminado

    def visualizar_pila(self):
        if self.es_vacia():
            print("La pila está vacía.")
            return
        nodo_iter = self.cima
        print("Contenido de la pila:")
        indice = 0
        while nodo_iter is not None:
            print(f"[{indice}] {nodo_iter}")
            nodo_iter = nodo_iter.siguiente
            indice += 1

    def obtener_por_indice(self, indice):
        nodo_iter = self.cima
        actual_indice = 0
        while nodo_iter is not None:
            if actual_indice == indice:
                return nodo_iter
            nodo_iter = nodo_iter.siguiente
            actual_indice += 1
        return None