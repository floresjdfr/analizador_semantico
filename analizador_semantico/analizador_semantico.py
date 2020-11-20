from parsing import Parsing
from tokenizer import tokenize
import queue
import re

class AnalisadorSemantico:

    '''
    Clase principal encargada de llevar a cabo el parsing y ademas analizar la semantica de la declaraciones de 
    funciones, varibales, condicionales, entre otras.
    '''
    def __init__(self, nombre_archivo):
        self._parsing = Parsing()
        self._lista_tokens = []
        self._tokenize(nombre_archivo)
    
    def _tokenize(self, _nombre_archivo):
        archivo = open(_nombre_archivo, 'r')
        contador_linea = 1
        for linea in archivo.readlines():
            tokens = tokenize(linea)
            self._lista_tokens.append({'linea':contador_linea, 'tokens':tokens})
            contador_linea += 1

    def analizar(self):
        self.parse()
        tabla = self._parsing.obtenerTabla()
        self._analisis_semantico_declaraciones(tabla)
        self._analisis_semantico_identificadores(tabla)
    
    def parse(self):
        for i in self._lista_tokens:
            linea = i['linea']
            tokens = i['tokens']
            self._parsing.parse(tokens, linea)
    
    def analisis_semantico_declaraciones(self, tabla): 
        self._analisis_semantico_declaraciones(tabla)
        
    def _analisis_semantico_identificadores(self, tabla):
        interes = {'int', 'string', 'float', 'identificador'}
        #x = y
        #(x, identificador), (=, asignacion), (y, identificador),(+, operador), (5, int)
        for tokens in self._lista_tokens:
            if (tokens['tokens']):
                resultado = self._analizador_elementos(tokens['tokens'])

                if resultado == 'ASIGNACION':
                    llave = tabla.buscar_simbolo(tokens['tokens'][0][0]) #verifica que la variable que esta a la izquierda del 
                                                                #operador de asignacion este en la tabla
                    if llave:
                        lista_asignaciones = self._extraer_asignaciones(tokens['tokens'])
                        #(y: identicador), (5, int)
                        for asignacion in lista_asignaciones:
                            if asignacion[1] == 'identificador':
                                valor = tabla.buscar_simbolo(asignacion[0]) #se verifica que la variable que va a ser asignada este en la tabla
                                if valor:
                                    if not valor['tipo'] == llave['tipo']: #si la variable esta en la tabla se verifica que sea del mismo tipo
                                        salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(tokens['linea'], valor['tipo'])
                                        print(salida)
                            else: #si no es una variable es un tipo dato primitivo
                                tipo_valor = self._tipo_dato_checker(llave['tipo'], asignacion[0])
                                if not tipo_valor:
                                    salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(tokens['linea'], llave['tipo'])
                                    print(salida)
                    else:
                        salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], tokens['tokens'][0][0])
                        print(salida)
                elif resultado == 'CONDICIONAL':
                    lista_asignaciones = self._extraer_asignaciones(tokens['tokens'])
                    if len(lista_asignaciones) > 1: #caso en que hayan dos elementos comparados
                        if lista_asignaciones[0][1] == 'identificador' and lista_asignaciones[1][1] == 'identificador': #caso de que ambos elementos sean variables
                            elemento1 = tabla.buscar_simbolo(lista_asignaciones[0][0])
                            elemento2 = tabla.buscar_simbolo(lista_asignaciones[1][0])
                            if not elemento1 or not elemento2:
                                if not elemento1:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], lista_asignaciones[0][0])
                                    print(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], lista_asignaciones[1][0])
                                    print(salida)
                        elif lista_asignaciones[0][1] == 'identificador' or lista_asignaciones[1][1] == 'identificador': #caso de que solo haya una variable y el otro sea algun tipo de dato primitivo
                            elemento1 = lista_asignaciones[0]
                            elemento2 = lista_asignaciones[1]
                            if elemento1[1] == 'identificador':
                                encontrado = tabla.buscar_simbolo(elemento1[0])
                                if encontrado:
                                    if not elemento2[1] == encontrado['tipo']:
                                        salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(tokens['linea'], encontrado['tipo'])
                                        print(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], elemento1[0])
                                    print(salida)
                            else:
                                encontrado = tabla.buscar_simbolo(elemento2[0])
                                if encontrado:
                                    if not elemento1[1] == encontrado['tipo']:
                                        salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(tokens['linea'], encontrado['tipo'])
                                        print(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], elemento2[0])
                                    print(salida)
                        else:
                            elemento1 = lista_asignaciones[0]
                            elemento2 = lista_asignaciones[1]
                            if not elemento1[1] == elemento2[2]:#caso de que los datos primitivos no sean del mismo tipo
                                salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(tokens['linea'], elemento1[1])
                                print(salida)
                    else: #en caso de que el condicional solo tenga un elemento dentro
                        if lista_asignaciones[0][1] == 'identificador':#caso de que ambos elementos sean variables
                            elemento1 = tabla.buscar_simbolo(lista_asignaciones[0][0])
                            if not elemento1:
                                salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], lista_asignaciones[0][0])
                                print(salida)
                        '''
                        else: #puede ser innecesario
                            elemento1 = lista_asignaciones[0]
                            encontrado = tabla.buscar_simbolo(elemento1[0])
                            if not encontrado:
                                print('Error')
                        '''

    def _extraer_asignaciones(self, linea_token):

        #[(x, identificador), (=, asignacion),(y, identificador),(+, operador_aritmentico), (z, identificador),(-, operador-aritmentico), (5, int)]
        interes = {'identificador', 'int', 'string', 'float'}
        lista_asignaciones = []
        for i in range(0, len(linea_token)):
            if linea_token[i][1] in interes:
                lista_asignaciones.append(linea_token[i])
        return lista_asignaciones

    def _analizador_elementos(self, tokens):
        operador_asignacion = False
        condicional = False
        parentesis_abre = False
        parentesis_cierra = False
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
            if token[1] == 'condicicional':
                condicional = True

        if  condicional and parentesis_abre:
            return 'CONDICIONAL'
        elif operador_asignacion and not palabra_tipo:
            return 'ASIGNACION'
        else:
            return 'NONE'
    
    def _analisis_semantico_declaraciones(self, tabla):
        errores = queue.Queue()
        
        for key, value in tabla.obtener_tabla().items():
            tipo = value['tipo']
            valor = value['valor']
            if valor:
                if self._tipo_dato_checker(tipo, valor):
                    continue
                else:
                    errores.put(value)
        if not errores.empty():
            while not errores.empty():
                value = errores.get()
                salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(value['linea'], value['tipo'])
                print(salida)
    
    def _obtener_tabla(self):
        return self._parsing.obtenerTabla()

    def _tipo_dato_checker(self, tipo, valor):
        if tipo == 'int':
            return self._verifica_int(valor)
        elif tipo == 'float':
            return self._verifica_float(valor)
        elif tipo == 'string':
            return self._verifica_string(valor)

    def _verifica_int(self, int):
        return int.isdigit()
    
    def _verifica_float(self, entrada):
            try:
                float(entrada)
                return True
            except ValueError:
                return False
    
    def _verifica_string(self, entrada):
        token = re.compile(r'"[a-zA-Z0-9_]*"')
        objeto_encontrado = token.match(entrada)
        if objeto_encontrado:
            return True
        return False
    