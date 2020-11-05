import parser
import tabla_simbolos


if __name__ == '__main__':

    archivo = open("codigo1.txt", 'r')

    for linea in archivo.readlines():
        print(linea)