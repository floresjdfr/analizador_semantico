class TablaSimbolos:

    def __init__(self):
        self.simbolos = {}
    
    def agregar_simbolo(self, llave, valor):

        for key in self.simbolos:
            if key == llave:
                self.simbolos[key] = valor
                return

        self.simbolos[llave] = valor
    
    def buscar_simbolo(self, llave):
        for key in self.simbolos:
            if key == llave:
                return self.simbolos[key]
        
        raise Exception("Symbol not defined")

    def imprimir(self):
        for key, value in self.simbolos.items():
            print(key, ' : ', value)