class Nodo:
    def __init__(self, root, valor):
        self._root = root
        self._valor = valor
        self._hijos = []

    def tieneHijos(self):
        return True if len(self._hijos) > 0 else False
    
    def agregarHijo(self, nuevo_elemento):
        self._hijo.append(Nodo(self, nuevo_elemento))
    
    def obtener_valor(self):
        return self._valor
    
    def obtener_padre(self):
        return self._root
        
    def obtener_nodo_actual(self):
        return self

