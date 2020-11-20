from tabla_simbolos import TablaSimbolos
import queue

class Parsing():

    '''
    Esta clase se encarga de utilizar una tabla de simbolos para clasificar los tokens recibidos
    '''
    def __init__(self):
        self._pila = queue.LifoQueue()
        self._pila.put("global")
        self._tabla_simbolos = TablaSimbolos()
  
    def parse(self, tokens, linea):
        if tokens:
            resultado = self._analizador_elementos(tokens)
            if resultado == 'RETURN':
                return self._return(tokens, linea)

            if resultado == 'DECLARACION_VARIABLE':
                self._declaracion_variable(tokens, linea)

            elif resultado == 'FUNCION':
                self._funcion(tokens, linea)

            elif resultado == "CIERRA_AMBITO":
                self._pila.get()

            elif resultado == 'CONDICIONAL':
                ambito = 'condicional_' + tokens[0][0]
                self._pila.put(ambito)
        return ""

    def imprimir_tabla(self):
        self._tabla_simbolos.imprimir()

    def _analizador_elementos(self, tokens):
        '''
        Utiliza varias banderas para poder identificar el tipo de linea de codigo leida (recivida por parametro en forma de token)
        '''
        operador_asignacion = False
        condicional = False
        parentesis_abre = False
        parentesis_cierra = False
        llaves_abre = False
        llaves_cierra = False
        palabra_tipo = False
        _return = False

        for token in tokens:
            if token[1] == 'return':
                _return = True 
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
            if token[1] == 'condicicional':
                condicional = True
        if _return:
            return 'RETURN'
        elif operador_asignacion and not parentesis_abre and palabra_tipo:
            return 'DECLARACION_VARIABLE'
        elif parentesis_abre and operador_asignacion and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and not condicional and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and condicional:
            return 'CONDICIONAL'
        elif operador_asignacion and not palabra_tipo and not condicional:
            return 'ASIGNACION'
        elif llaves_cierra:
            return 'CIERRA_AMBITO'
        else:
            return 'NONE'

    def _declaracion_variable(self, tokens, linea):
        tipo = tokens[0][0]
        identificador = tokens[1][0]
        valor = None
        if len(tokens) > 2:
            valor = tokens[3][0]
        ambito = self._pila.get()
        self._pila.put(ambito)
        valor = {'tipo':tipo, 'valor':valor, 'linea':linea, 'ambito':ambito}
        self._tabla_simbolos.agregar_simbolo(identificador, valor)

    def _return(self, tokens, linea):
        if len(tokens) > 1:
            elemento_retornado =  tokens[1]
            if elemento_retornado[1] == 'identificador':
                elemento_en_tabla = self._tabla_simbolos.buscar_simbolo(elemento_retornado[0])
                if elemento_en_tabla:
                    ambito = self._pila.get()
                    self._pila.put(ambito)
                    funcion = self._tabla_simbolos.buscar_simbolo(ambito)
                    if not elemento_en_tabla['tipo'] == funcion['tipo']:
                        salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(linea, ambito)
                        return salida
                        #print(salida)
                else:
                    salida = "Error - linea: {}. '{}' no esta declarado.".format(linea, elemento_retornado[0])
                    print(salida)
            else:
                ambito = self._pila.get()
                self._pila.put(ambito)
                funcion = self._tabla_simbolos.buscar_simbolo(ambito)
                if not elemento_retornado[1] == funcion['tipo']:
                    salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(linea, ambito)
                    return salida
                    #print(salida)
        else:
            ambito = self._pila.get()
            self._pila.put(ambito)
            funcion = self._tabla_simbolos.buscar_simbolo(ambito)
            if not funcion['tipo'] == 'void':
                salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(linea, ambito)
                return salida
                #print(salida)
        return ""
    
    def _funcion(self, tokens, linea):
        tipo = tokens[0][0]
        identificador = tokens[1][0]
        ambito = self._pila.get()
        self._pila.put(ambito)
        valor = {'tipo':tipo, 'valor':None, 'linea':linea, 'ambito':ambito}
        self._tabla_simbolos.agregar_simbolo(identificador, valor)
        
        ambito = identificador
        self._pila.put(ambito)

        parametros = self._extraer_parametros(tokens)

        while len(parametros) > 0:
            parametro = parametros.pop(0)
            tipo = parametro[0]
            identificador = parametro[1]
            valor = None
            if len(parametro) > 2:
                valor = parametro[4]
            ambito = self._pila.get()
            self._pila.put(ambito)
            valor = {'tipo':tipo, 'valor':valor, 'linea':linea, 'ambito':ambito}
            self._tabla_simbolos.agregar_simbolo(identificador, valor)

    def _extraer_parametros(self, linea):

        '''
        Utilizado para extraer los parametros que se encuentran entre parentesis en una funcion
        '''
        lista_parametros = [] #se guardan los parametros de la linea de tokens
        parametro_auxiliar = []

        for i in range(3, len(linea)+1): #recorre la linea de tokens
            if linea[i][1] is 'parentesis': #si el token vuelve a ser un parentesis significa que es el parentesis que cierra
                if len(parametro_auxiliar) > 0:
                    lista_parametros.append(parametro_auxiliar) #lo que este en parametro_auxiliar se agrega a la lista de parametros
                    break
            elif linea[i][1] is 'coma': #si el token es una coma todo lo que este en el parametro_auxiliar se agrega a la lista de parametros
                if len(parametro_auxiliar) > 0:
                    lista_parametros.append(parametro_auxiliar)
                    parametro_auxiliar = []
            elif linea[i][1] is not 'coma': #si el token actual no es una coma, es parte del parametro (tipo, identificador, =, valor)
                parametro_auxiliar.append(linea[i][0]) #se agrega al parameto_auxiliar
        return lista_parametros
    
    def obtenerTabla(self):
        return self._tabla_simbolos