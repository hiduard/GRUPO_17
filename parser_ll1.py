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

class ParserLL1:
    def __init__(self, fluxo_promovido, linhas, fontes, tabela):
        self.tokens = fluxo_promovido
        self.linhas = linhas     
        self.fontes = fontes      
        self.tabela = tabela
        self.i = 0
        self.derivacoes = []

    def lookahead(self):
        if self.i >= len(self.tokens):
            return "$"
        return self.tokens[self.i][0]

    def linhaAtual(self):
        if self.i >= len(self.linhas):
            return self.linhas[-1] if self.linhas else 0
        return self.linhas[self.i]

    def fonteAtual(self):
        return self.fontes.get(self.linhaAtual(), "")

    def erro(self, mensagem):
        linha = self.linhaAtual()
        fonte = self.fonteAtual()
        la = self.lookahead()
        raise ValueError(
            f"Erro sintatico na linha {linha} (lookahead={la}): {mensagem}"
            f" — trecho: {fonte}"
        )

    def consumir(self, esperado):
        if self.lookahead() != esperado:
            self.erro(f"esperava '{esperado}', encontrei '{self.lookahead()}'")
        valor = self.tokens[self.i][1]
        self.i += 1
        return valor

    def registrarDerivacao(self, nao_terminal, regra):
        self.derivacoes.append({
            "nao_terminal": nao_terminal,
            "lookahead": self.lookahead(),
            "regra": list(regra),
        })

    def escolherProducao(self, nao_terminal):
        la = self.lookahead()
        regra = self.tabela.get(nao_terminal, {}).get(la)
        if regra is None:
            self.erro(
                f"sem producao LL(1) para nao-terminal '{nao_terminal}' "
                f"com lookahead '{la}'"
            )
        self.registrarDerivacao(nao_terminal, regra)
        return regra

    def parse_programa(self):
        self.escolherProducao("programa")
        self.parse_abre_start()
        comandos = self.parse_lista("lista_prog")
        linha_fim = self.parse_fecha_end()
        linha_inicio = 1 if not self.linhas else self.linhas[0]
        return {
            "tipo": "programa",
            "linha_inicio": linha_inicio,
            "linha_fim": linha_fim,
            "comandos": comandos,
        }

    def parse_abre_start(self):
        self.escolherProducao("abre_start")
        self.consumir("LPAREN_CMD")
        self.consumir(START)
        self.consumir(RPAREN)

    def parse_fecha_end(self):
        self.escolherProducao("fecha_end")
        linha = self.linhaAtual()
        self.consumir("LPAREN_END")
        self.consumir(END)
        self.consumir(RPAREN)
        return linha

    def parse_lista(self, nome_nt):
        comandos = []
        while True:
            regra = self.escolherProducao(nome_nt)
            if regra == ["epsilon"]:
                return comandos
            comandos.append(self.parse_comando())