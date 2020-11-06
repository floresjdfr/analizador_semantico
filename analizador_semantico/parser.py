from leer_archivo import leer_archivo
from Arbol import Nodo
import queue

class Parser():
    def __init__(self):
        self._pila = queue.LifoQueue()
        self._elementos = []

    def parse1(self, tokens):
        tipo = None
        identificador = None
        valor = None
        if tokens[0][0] is 'tipo_dato':
            tipo = tokens[0][0]
            identificador = tokens[1][0]
            if len(tokens) > 2:
                if tokens[2][0] is '=':
                    valor = tokens[3][0]
                else:
                    valor = None
            else:
                valor = None

        diccionarioPrueba = {'Identificador': {'tipo': tipo, 'Valor' : valor, 'Ambito' : 'global', 'Linea': 0}}
        
        return diccionarioPrueba


            
        

#[('int', 'tipo_dato'), ('x', 'variable'), ('=', 'operador_logico'), ('40', 'int')]
    def parse(self, tokens):
        for token in tokens:
            if token[1] == 'tipo_dato': #si el token es una palabra reservada indica una nueva declaracion de variable o funcion
                if len(self._elementos) > 0:
                    if len(self._elementos) > 2:
                        tipo = self._elementos[0]
                        identificador = self._elementos[1]
                        valor = self._elementos[3]
                    else:
                        tipo = self._elementos[0]
                        identificador = self._elementos[1]
                        valor = None
                         
                else:
                    self._elementos.append(token[0])
            
            else:
                self._elementos.append(token[0])
        if len(self._elementos) > 0:
            pass
        

#ejemplo tokens recibidos
'''
['int', 'x', '=' '40']
['void', 'funcion', '(', 'float', 'v', 'string',')','{']
['if', '(', 'v', '0.0', '{']
['n', '=', '"Mayor"']
['x', '=', 'x', '+', '5']
'''

'''
    def check_token(token):

        

        
        

        elif token in parentesis: #si el token es un parentesis indica que es una funcion
            tipo_parentesis = None
            for key, value in parentesis: #este ciclo optiene el tipo de parentesis
                if token == value:
                    tipo_parentesis = key
            if tipo_parentesis == 'abre':
                if not es_condicional:
                    es_funcion = True
                    nuevo_elemento = ''.join(' '.join(i) for i in elementos)
                    nuevo_ambito = Nodo(ambito_actual, nuevo_elemento)
                    ambito_actual.agregarHijo(nuevo_ambito)
                    ambito_actual = nuevo_ambito
                    elementos.clear()
            elif tipo_parentesis == 'cierra': #si el parentesis cierra no pasa nada
                pass

        elif token in llaves: # si el token esta en llaves indica que abre declaraciones de una funcion o condicional o si este cierra indica que las variables declaradas acaban su ambito
            tipo_llave = None
            for key, value in llaves: #este ciclo optiene el tipo de parentesis
                if token == value:
                    tipo_parentesis = key

            if tipo_llave == 'abre': # si la llave abre no pasa nada
                pass
            if tipo_llave == 'cierra': # si la llave cierra se vuelve al ambito anterior
                if len(elementos) > 0:
                    nuevo_elemento = ''.join(' '.join(i) for i in elementos)
                    ambito_actual.agregarHijo(nuevo_elemento)
                    elementos.clear()
                    ambito_actual = ambito_actual.obtener_padre()
                    if es_condicional:
                        es_condicional = False
                    elif es_funcion:
                        es_funcion = False
                else:
                    if es_condicional:
                        es_condicional = False
                    elif es_funcion:
                        es_funcion = False

        elif token in condicionales: #si el token es algun condicional, este condicional seria un nuevo ambito para las variables declaradas dentro de este
            if len(elementos) > 0:#si por alguna razon la lista de elementos no esta vacia, agrego los elementos como hijo del ambito actual
                    nuevo_elemento = ''.join(' '.join(i) for i in elementos)
                    ambito_actual.agregarHijo(nuevo_elemento)
                    elementos.clear()

                    nuevo_elemento = token + "_condicional"
                    
                    nuevo_ambito = Nodo(ambito_actual, nuevo_elemento)
                    ambito_actual.agregarHijo(nuevo_ambito)
                    ambito_actual = nuevo_ambito
            else:
                es_condicional = True
                nuevo_elemento = token + "_condicional"
                    
                nuevo_ambito = Nodo(ambito_actual, nuevo_elemento)
                ambito_actual.agregarHijo(nuevo_ambito)
                ambito_actual = nuevo_ambito

        else:
            elementos.append(token)



'''

    