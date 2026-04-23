# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17


def lerArquivo(nomeArquivo):
    resultado = []
    with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            conteudo = linha.strip()
            if conteudo:
                resultado.append((numero, conteudo))
    return resultado
