class TablaSimbolos:

    def __init__(self):
        self.simbolos = dict()
    
    def agregar_simbolo(self, llave, valor):

        for key in TablaSimbolos.simbolos:
            if key == llave:
                TablaSimbolos.simbolos[key] = valor
                return

        TablaSimbolos.simbolos[llave] = valor

    
    
    def buscar_simbolo(self, llave):
        for key in TablaSimbolos.simbolos:
            if key == llave:
                return TablaSimbolos.simbolos[key]
        
        raise Exception("Symbol not defined")