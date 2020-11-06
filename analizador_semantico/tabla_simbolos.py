import queue
import re

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
#{tipo:x,valor:x,linea:x, ambito:x}
    
    def analisis_semantico(self):
        errores = queue.Queue()

        for key, value in self.simbolos.items():
            tipo = value['tipo']
            valor = value['valor']
            if valor:
                if self.tipo_checker(tipo, valor):
                    continue
                else:
                    errores.put(value)
        if not errores.empty():
            while not errores.empty():
                value = errores.get()
                salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(value['linea'], value['tipo'])
                print(salida)
            
    def tipo_checker(self, tipo, valor):
        if tipo == 'int':
            return self.verifica_int(valor)
        elif tipo == 'float':
            return self.verifica_float(valor)
        elif tipo == 'string':
            return self.verifica_string(valor)
        

                
    def verifica_int(self, int):
        return int.isdigit()
    
    def verifica_float(self, entrada):
            try:
                float(entrada)
                return True
            except ValueError:
                return False
    
    def verifica_string(self, entrada):
        token = re.compile(r'"[a-zA-Z0-9_]*"')
        objeto_encontrado = token.match(entrada)
        if objeto_encontrado:
            return True
        return False

    def imprimir(self):
        for key, value in self.simbolos.items():
            print(key, ' : ', value)
'''
#{tipo:x,valor:x,linea:x, ambito:x}
tabla = TablaSimbolos()
tabla.agregar_simbolo('ident1',{'tipo': 'int', 'valor':'ete sech', 'linea':'1', 'ambito': 'global'})
tabla.agregar_simbolo('ident2',{'tipo': 'float', 'valor':'el pepe', 'linea':'2', 'ambito': 'global'})
tabla.agregar_simbolo('ident3',{'tipo': 'string', 'valor':'7.7', 'linea':'3', 'ambito': 'global'})
tabla.agregar_simbolo('ident4',{'tipo': 'string', 'valor':'"5"', 'linea':'5', 'ambito': 'global'})

tabla.analisis_semantico()
'''