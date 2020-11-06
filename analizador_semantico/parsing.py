from leer_archivo import leer_archivo
from Arbol import Nodo
import queue

class Parsing():
    def __init__(self):
        self._pila = queue.LifoQueue()
        self._elementos = []


    def extraer_parametros(self, linea):
        lista_parametros = [] #se guardan los parametros de la linea de tokens
        parametro_auxiliar = ""

        for i in range(3, len(linea)+1): #recorre la linea de tokens
            if linea[i][1] is not 'coma': #si el token actual no es una coma, es parte del parametro (tipo, identificador, =, valor)
                parametro_auxiliar.join(" " + i[i][0]) #se agrega al parameto_auxiliar

            elif linea[i][1] is 'coma': #si el token es una coma todo lo que este en el parametro_auxiliar se agrega a la lista de parametros
                if len(parametro_auxiliar) > 0:
                    lista_parametros.append(parametro_auxiliar)
                    parametro_auxiliar = ""
            
            elif linea[i][1] is 'parentesis': #si el token vuelve a ser un parentesis significa que es el parentesis que cierra
                if len(parametro_auxiliar) > 0:
                    lista_parametros.append(parametro_auxiliar) #lo que este en parametro_auxiliar se agrega a la lista de parametros
                    break
        return lista_parametros
          
    def parse(self, tokens):
        resultado = self.analizador_elementos(tokens)
        if resultado == 'DECLARACION_VARIABLE':
            tipo = tokens[0][0]
            identificador = [1][0]
            elemento = [3][0]
        if resultado == 'FUNCION':
            tipo = tokens[0][0]
            identificador = [1][0]
        if resultado == 'CONDICIONAL':
            pass
        
    def analizador_elementos(self, tokens):
        operador_asignacion = False
        condicional = False
        parentesis_abre = False
        parentesis_cierra = False
        llaves_abre = False
        llaves_cierra = False
        palabra_tipo = False

        for token in tokens:
            if token[1] == 'tipo':
                palabra_tipo = True
            if token[1] == 'asignacion':
                operador_asignacion = True
            if token[1] == 'parentesis':
                if token[0] == '(':
                    parentesis_abre = True
                else:
                    parentesis_cierra = True
            if token[1] == 'llave':
                if token[0] == '{':
                    llaves_abre = True
                else:
                    llaves_cierra = True
            if token[1] == 'palabra_reservada':
                condicional = True

        if operador_asignacion and not parentesis_abre and palabra_tipo:
            return 'DECLARACION_VARIABLE'
        elif parentesis_abre and operador_asignacion and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and not condicional and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and condicional:
            return 'CONDICIONAL'
        elif operador_asignacion and not palabra_tipo and not condicional:
            return 'ASIGNACION'
        else:
            return 'NONE'
    
    
    