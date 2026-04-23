# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

import sys
import json
import os

from gramatica import construirGramatica
from parser_ll1 import parsear
from arvore import gerarArvore, arvoreParaTexto, salvarArvoreJSON, salvarArvoreTexto
from assembly import gerarAssembly
from utils import lerTokens, salvarTokens
from leitor import lerArquivo
from lexico import parseExpressao


def garantir_pasta(caminho):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        print("Exemplo: python main.py teste1.txt")
        return

    nome_arquivo = sys.argv[1]

    if not os.path.isfile(nome_arquivo):
        print(f"Erro: arquivo '{nome_arquivo}' nao encontrado.")
        return

    tokens_por_linha = []
    gramatica = construirGramatica()
    resultado = parsear(tokens_por_linha, gramatica["tabela"])
    arvore = gerarArvore(resultado)
    codigo = gerarAssembly(arvore)


if __name__ == "__main__":
    main()