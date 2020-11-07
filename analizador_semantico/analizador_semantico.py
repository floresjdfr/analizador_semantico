from parsing import Parsing
from tokenizer import tokenize
import queue
import re

class AnalisadorSemantico:
    def __init__(self, nombre_archivo):
        self._parsing = Parsing()
        self._lista_tokens = []
        self._tokenize(nombre_archivo)
    
    def _tokenize(self, _nombre_archivo):
        archivo = open(_nombre_archivo, 'r')
        contador_linea = 1
        for linea in archivo.readlines():
            tokens = tokenize(linea)
            self.lista_tokens.append({'linea':contador_linea, 'tokens':tokens})
            contador_linea += 1

    def parse(self):
        for i in self._lista_tokens:
            linea = i['linea']
            tokens = i['linea_tokens']
            self._parsing.parse(tokens, linea)
    
    def analisis_semantico_declaraciones(self): #listo
        tabla = self._obtener_tabla()
        self._analisis_semantico_declaraciones(tabla)
        
    def _analisis_identificadores(self, tabla):
        interes = {'int', 'string', 'float', 'identificador'}
        operador = {'+', '-'}
        tabla = self._obtener_tabla()
        #x = y
        #(x, identificador), (=, asignacion), (y, identificador),(+, operador), (5, int)
        for tokens in self._lista_tokens:
            resultado = self._analizador_elementos(tokens)
            if resultado == 'ASIGNACION':
                llave = tabla.buscar_simbolo(tokens[0][0])
                if llave:
                    lista_asignaciones = self._extraer_asignaciones(tokens)
                    #(y: identicador), (5, int)
                    for asignacion in lista_asignaciones:
                        if asignacion[1] == 'identificador':
                            valor = tabla.buscar_simbolo(asignacion[0])
                            if valor:
                                if not valor['tipo'] == llave['tipo']:
                                    print("Error")
                        else:
                            tipo_valor = self._tipo_dato_checker(llave['tipo'], asignacion[0])
                            if not tipo_valor:
                                print("Error")
                else:
                    print("Error")

    def _extraer_asignaciones(self, linea_token):
        #[(x, identificador), (=, asignacion),(y, identificador),(+, operador_aritmentico), (z, identificador),(-, operador-aritmentico), (5, int)]
        interes = {'identificador', 'int', 'string', 'float'}
        lista_asignaciones = []
        for i in range(2, len(linea_token)+1):
            if linea_token[i][1] in interes:
                lista_asignaciones = linea_token[i]
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
            if token[1] == 'palabra_reservada':
                condicional = True

        if  condicional and parentesis_abre:
            return 'CONDICIONAL'
        elif operador_asignacion and not palabra_tipo:
            return 'ASIGNACION'
        else:
            return 'NONE'
    
    def _analisis_semantico_declaraciones(self, tabla):
        errores = queue.Queue()

        for key, value in tabla.items():
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
    