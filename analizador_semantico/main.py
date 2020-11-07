from parsing import Parsing
from tokenizer import tokenize

if __name__ == '__main__':

    archivo = open("codigo2.txt", 'r')

    pars = Parsing()
    #lista_tokens -= [{'linea': 1, 'linea_tokens': tokens}, {'linea': 2, 'linea_tokens': tokens}]
    contador_linea = 1
    lista_tokens = []
    for linea in archivo.readlines():
        token = tokenize(linea)
        contador_linea += 1
        lista_tokens.append({'linea':contador_linea, 'linea_tokens':token})
        
        
    
    pars.imprimir_tabla()
        
