# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

EPSILON = "epsilon"
EOF = "$"

TERMINAIS = {
    "LPAREN",
    "RPAREN",
    "NUMBER",
    "MEMORY",
    "OPERATOR",
    "REL_OP",
    "RES",
    "START",
    "END",
    "IF",
    "ELSE",
    "ENDIF",
    "WHILE",
    "ENDWHILE",
    EOF,
}

def construirGramatica():
    producoes = {
        "programa": [
            ["abre_start", "lista_prog", "fecha_end"],
        ],
        "abre_start": [
            ["LPAREN", "START", "RPAREN"],
        ],
        "fecha_end": [
            ["LPAREN", "END", "RPAREN"],
        ],

        "lista_prog": [
            ["comando", "lista_prog"],
            [EPSILON],
        ],
        "lista_if": [
            ["comando", "lista_if"],
            [EPSILON],
        ],
        "lista_while": [
            ["comando", "lista_while"],
            [EPSILON],
        ],

        "comando": [
            ["LPAREN", "interior"],
        ],

        "interior": [
            ["NUMBER", "apos_num"],
            ["MEMORY", "apos_mem"],
            ["LPAREN", "sub", "apos_sub"],
        ],

        "apos_num": [
            ["RES", "RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN", "sub", "resto_sub"],
        ],
        "apos_mem": [
            ["RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN", "sub", "resto_sub"],
        ],
        "apos_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num"],
            ["MEMORY", "resto_mem_grava"],
            ["LPAREN", "sub", "resto_sub"],
        ],

        "resto_num": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],
        "resto_mem_grava": [
            ["RPAREN"],
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],
        "resto_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "cauda_rel"],
        ],

        "cauda_rel": [
            ["RPAREN"],
            ["IF", "RPAREN", "lista_if", "fim_if"],
            ["WHILE", "RPAREN", "lista_while", "abre_endwhile"],
        ],

        "fim_if": [
            ["abre_else", "lista_if", "abre_endif"],
            ["abre_endif"],
        ],

        "abre_else": [
            ["LPAREN", "ELSE", "RPAREN"],
        ],
        "abre_endif": [
            ["LPAREN", "ENDIF", "RPAREN"],
        ],
        "abre_endwhile": [
            ["LPAREN", "ENDWHILE", "RPAREN"],
        ],

        "sub": [
            ["NUMBER", "apos_num_sub"],
            ["MEMORY", "apos_mem_sub"],
            ["LPAREN", "sub", "apos_sub_sub"],
        ],

        "apos_num_sub": [
            ["RES", "RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN", "sub", "resto_sub_sub"],
        ],
        "apos_mem_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN", "sub", "resto_sub_sub"],
        ],
        "apos_sub_sub": [
            ["RPAREN"],
            ["NUMBER", "resto_num_sub"],
            ["MEMORY", "resto_mem_grava_sub"],
            ["LPAREN", "sub", "resto_sub_sub"],
        ],

        "resto_num_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
        "resto_mem_grava_sub": [
            ["RPAREN"],
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
        "resto_sub_sub": [
            ["OPERATOR", "RPAREN"],
            ["REL_OP", "RPAREN"],
        ],
    }

    nao_terminais = set(producoes.keys())
    first = calcularFirst(producoes, nao_terminais)
    follow = calcularFollow(producoes, nao_terminais, first, "programa")


    return {
        "simbolo_inicial": "programa",
        "producoes": producoes,
        "nao_terminais": nao_terminais,
        "terminais": TERMINAIS,
        "first": first,
        "follow": follow,
    }

def calcularFirst(producoes, nao_terminais):
    first = {nt: set() for nt in nao_terminais}

    mudou = True
    while mudou:
        mudou = False
        for A, regras in producoes.items():
            for regra in regras:
                first_seq = calcularFirstDaSequencia(regra, first, nao_terminais)
                tamanho_antes = len(first[A])
                first[A].update(first_seq)
                if len(first[A]) != tamanho_antes:
                    mudou = True

    return first

def calcularFirstDaSequencia(sequencia, first, nao_terminais):
    if not sequencia:
        return {EPSILON}

    resultado = set()

    for simbolo in sequencia:
        if simbolo == EPSILON:
            resultado.add(EPSILON)
            return resultado

        if simbolo not in nao_terminais:
            resultado.add(simbolo)  
            return resultado

        resultado.update(first[simbolo] - {EPSILON})

        if EPSILON not in first[simbolo]:
            return resultado

    resultado.add(EPSILON)
    return resultado

def calcularFollow(producoes, nao_terminais, first, simbolo_inicial):
    follow = {nt: set() for nt in nao_terminais}
    follow[simbolo_inicial].add(EOF)

    mudou = True
    while mudou:
        mudou = False
        for A, regras in producoes.items():
            for regra in regras:
                for i, B in enumerate(regra):
                    if B not in nao_terminais:
                        continue

                    beta = regra[i + 1:]
                    first_beta = calcularFirstDaSequencia(beta, first, nao_terminais)

                    tamanho_antes = len(follow[B])
                    follow[B].update(first_beta - {EPSILON})

                    if EPSILON in first_beta or len(beta) == 0:
                        follow[B].update(follow[A])

                    if len(follow[B]) != tamanho_antes:
                        mudou = True

    return follow

def formatarRegra(A, regra):
    return f"{A} -> {' '.join(regra)}"