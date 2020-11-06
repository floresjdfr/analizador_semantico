from parsing import Parsing
from tokenizer import tokenize

if __name__ == '__main__':

    archivo = open("codigo2.txt", 'r')

    pars = Parsing()

    contador_linea = 1
    for linea in archivo.readlines():
        linea_tokenized = tokenize(linea)
        pars.parse(linea_tokenized, contador_linea)
        contador_linea += 1
    
    pars.imprimir_tabla()
        
