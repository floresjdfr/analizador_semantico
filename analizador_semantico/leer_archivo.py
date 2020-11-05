import tokenizer

def leer_archivo(nombre_archivo):
    archivo = open(nombre_archivo, 'r')

    for linea in archivo.readlines():
        lista = tokenizer.tokenize(linea)
        print(lista)
        print()

leer_archivo("codigo2.txt")