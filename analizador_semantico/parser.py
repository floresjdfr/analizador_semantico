from leer_archivo import leer_archivo
from Arbol import Nodo
archivo = 'codigo1.txt'

tokens = leer_archivo(archivo)

reservadas = {'void, int, string, return, float'}
llaves = {'abre':'{', 'cierra':'}'}
parentesis = {'abre':'(', 'cierra': ')'}
condicionales = {'if', 'while'}

es_funcion = False
es_condicional = False


elementos = []

ambito_actual = Nodo(None, "global")

#ejemplo tokens recibidos
'''
['int', 'x', '=' '40']
['void', 'funcion', '(', 'float', 'v', 'string',')','{']
['if', '(', 'v', '0.0', '{']
['n', '=', '"Mayor"']
['x', '=', 'x', '+', '5']
'''


def check_token(token):

    global es_funcion
    global es_condicional
    global elementos
    global ambito_actual

    
    if token in reservadas: #si el token es una palabra reservada indica una nueva declaracion de variable o funcion
        if len(elementos) > 0: 
            if not es_funcion:
                nuevo_elemento = ''.join(' '.join(i) for i in elementos)
                ambito_actual.agregarHijo(nuevo_elemento)
                elementos.clear()
            elif es_funcion:
                if len(elementos) > 0:
                    nuevo_elemento = ''.join(' '.join(i) for i in elementos)
                    ambito_actual.agregarHijo(nuevo_elemento)
                    elementos.clear()
                else:
                    elementos.append(token)                    
        else:
            elementos.append(token)

    elif token in parentesis: #si el token es un parentesis indica que es una funcion
        tipo_parentesis = None
        for key, value in parentesis: #este ciclo optiene el tipo de parentesis
            if token == value:
                tipo_parentesis = key
        if tipo_parentesis == 'abre':
            es_funcion = True
            nuevo_elemento = ''.join(elementos)
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
                nuevo_elemento = ''.join(elementos)
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
                nuevo_elemento = ''.join(elementos)
                ambito_actual.agregarHijo(nuevo_elemento)
                elementos.clear()

                nuevo_elemento = token + "_condicional"
                
                nuevo_ambito = Nodo(ambito_actual, nuevo_elemento)
                ambito_actual.agregarHijo(nuevo_ambito)
                ambito_actual = nuevo_ambito
        else:
            nuevo_elemento = token + "_condicional"
                
            nuevo_ambito = Nodo(ambito_actual, nuevo_elemento)
            ambito_actual.agregarHijo(nuevo_ambito)
            ambito_actual = nuevo_ambito

    else:
        elementos.append(token)
        
                
def check_funcion(lista_elementos):
    if '{' in lista_elementos:
        return True
    return False





        
