import parser
import tabla_simbolos


if __name__ == '__main__':

    archivo = open("codigo1.txt", 'r')

    par1 = parser()

    ban = True
    for linea in archivo.readlines():
        if ban:
            print(par1.parse1(linea))
            ban = False
        print(linea)
