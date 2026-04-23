# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

from tokens import (
    LPAREN,
    RPAREN,
    NUMBER,
    MEMORY,
    OPERATOR,
    REL_OP,
    RES,
    START,
    END,
    IF,
    ELSE,
    ENDIF,
    WHILE,
    ENDWHILE,
    INVALID,
)

PROMOCAO_LPAREN = {
    END: "LPAREN_END",
    ELSE: "LPAREN_ELSE",
    ENDIF: "LPAREN_ENDIF",
    ENDWHILE: "LPAREN_ENDWHILE",
}

def promoverLParens(fluxo):
    promovido = []
    n = len(fluxo)

    for i in range(n):
        tipo, valor = fluxo[i]

        if tipo != LPAREN:
            promovido.append((tipo, valor))
            continue

        if i + 1 < n:
            proximo_tipo = fluxo[i + 1][0]
            classe = PROMOCAO_LPAREN.get(proximo_tipo, "LPAREN_CMD")
        else:
            classe = "LPAREN_CMD"

        promovido.append((classe, valor))

    return promovido