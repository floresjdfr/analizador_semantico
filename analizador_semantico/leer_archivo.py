import tokenizer

def leer_archivo(nombre_archivo):
    archivo = open(nombre_archivo, 'r')
    lista = None
    for linea in archivo.readlines():
        lista = tokenizer.tokenize(linea)
        print(lista)
        print()
    return lista
    

leer_archivo("codigo1.txt")