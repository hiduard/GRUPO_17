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

def salvar_resultado_parser(resultado, caminho):
    garantir_pasta(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(f"ACEITO: {resultado['aceito']}\n\n")

        if resultado.get("erros_lexicos"):
            arquivo.write("ERROS LEXICOS:\n")
            for e in resultado["erros_lexicos"]:
                arquivo.write(f"  {e}\n")
            arquivo.write("\n")
            return

        if resultado["erro"]:
            arquivo.write(f"ERRO SINTATICO: {resultado['erro']}\n\n")
            if resultado["derivacoes"]:
                arquivo.write("DERIVACOES APLICADAS ATE O ERRO:\n")
                for derivacao in resultado["derivacoes"]:
                    arquivo.write(json.dumps(derivacao, ensure_ascii=False))
                    arquivo.write("\n")
            return

        arquivo.write("DERIVACOES:\n")
        for derivacao in resultado["derivacoes"]:
            arquivo.write(json.dumps(derivacao, ensure_ascii=False))
            arquivo.write("\n")

def salvar_assembly(codigo, caminho):
    garantir_pasta(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(codigo)

def carregar_entrada(nome_arquivo):
    if nome_arquivo.endswith(".tok") or nome_arquivo.endswith(".tokens"):
        return lerTokens(nome_arquivo)

    linhas = lerArquivo(nome_arquivo) 
    tokens_por_linha = []
    for numero_linha, linha in linhas:
        tokens = parseExpressao(linha)
        tokens_por_linha.append((numero_linha, linha, tokens))
    return tokens_por_linha
       

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        return

    nome_arquivo = sys.argv[1]
    if not os.path.isfile(nome_arquivo):
        print(f"Erro: arquivo '{nome_arquivo}' nao encontrado.")
        return

    tokens_por_linha = carregar_entrada(nome_arquivo)
    gramatica = construirGramatica()
    resultado = parsear(tokens_por_lingua, gramatica["tabela"])

    salvarTokens(tokens_por_linha, "output/tokens_saida.txt")
    salvar_resultado_parser(resultado, "output/parser_resultado.txt")

    print(f"ACEITO: {resultado['aceito']}")

    if not resultado["aceito"]:
        return

    arvore = gerarArvore(resultado)
    salvarArvoreJSON(arvore, "output/arvore.json")
    salvarArvoreTexto(arvore, "output/arvore.txt")

    codigo = gerarAssembly(arvore)
    salvar_assembly(codigo, "output/programa.s")

if __name__ == "__main__":
    main()