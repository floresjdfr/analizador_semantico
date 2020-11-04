import re

def tokenizer(linea: str):
    expresiones_regulares = [
        (re.compile(r"(if|while|return)"), "palabras_reservada"),
        (re.compile(r"(void|int|float|string)"), "tipo_dato"),
        (re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"), "variable"),
        (re.compile(r"^[0-9]+"), "numero"),
        (re.compile(r"^[+*/-]"), "operador_aritmetico"),
        (re.compile(r"^[><=]"), "operador_logico"),
        (re.compile(r"^="), "asignacion"),
        (re.compile(r"^[()]"), "parentesis"),
        (re.compile(r"^[{}]"), "llave"),
    ]

    tokens = []

    while len(linea):
        linea = linea.lstrip()

        matched = False

        for token, tipo in expresiones_regulares:
            objeto_encontrado = token.match(linea)
            if objeto_encontrado:
                matched = True
                token = (objeto_encontrado.group(0), tipo)
                tokens.append(token)
                linea = linea.replace(token[0], '')
                linea = linea.lstrip()
                break  # break out of the inner loop

        if not matched:
            raise Exception("Invalid String " + linea)

    return tokens

linea = "int n = 123"
tokens = tokenizer(linea)
print(tokens)