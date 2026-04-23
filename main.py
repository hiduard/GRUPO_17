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

def salvar_gramatica_markdown(gramatica, caminho):
    garantir_pasta(caminho)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("# Gramatica LL(1)\n\n")

        arquivo.write("## Simbolo inicial\n\n")
        arquivo.write(f"`{gramatica['simbolo_inicial']}`\n\n")

        arquivo.write("## Producoes\n\n")
        arquivo.write(
            "Notacao EBNF: **nao-terminais em minusculas**, "
            "**TERMINAIS EM MAIUSCULAS**.\n\n"
        )
        for A, regras in gramatica["producoes"].items():
            for regra in regras:
                lado_direito = " ".join(regra)
                arquivo.write(f"- `{A} -> {lado_direito}`\n")
        arquivo.write("\n")

        arquivo.write("## FIRST\n\n")
        for nt in sorted(gramatica["first"]):
            conteudo = ", ".join(sorted(gramatica["first"][nt]))
            arquivo.write(f"- `FIRST({nt}) = {{ {conteudo} }}`\n")
        arquivo.write("\n")

        arquivo.write("## FOLLOW\n\n")
        for nt in sorted(gramatica["follow"]):
            conteudo = ", ".join(sorted(gramatica["follow"][nt]))
            arquivo.write(f"- `FOLLOW({nt}) = {{ {conteudo} }}`\n")
        arquivo.write("\n")

        arquivo.write("## Tabela LL(1)\n\n")
        for nt in sorted(gramatica["tabela"]):
            arquivo.write(f"### {nt}\n\n")
            for terminal, regra in sorted(gramatica["tabela"][nt].items()):
                lado_direito = " ".join(regra)
                arquivo.write(f"- `[{nt}, {terminal}] -> {lado_direito}`\n")
            arquivo.write("\n")

        arquivo.write("## Conflitos\n\n")
        if gramatica["conflitos"]:
            for conflito in gramatica["conflitos"]:
                A, terminal, antiga, nova = conflito
                arquivo.write(f"- Conflito em `{A}, {terminal}`: `{antiga}` x `{nova}`\n")
        else:
            arquivo.write("Sem conflitos LL(1).\n")

def salvar_gramatica_com_arvore(gramatica, arvore, caminho):
    salvar_gramatica_markdown(gramatica, caminho)
    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write("\n---\n\n")
        arquivo.write("## Arvore Sintatica (ultimo teste)\n\n")
        arquivo.write("```\n")
        arquivo.write(arvoreParaTexto(arvore))
        arquivo.write("\n```\n")

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
    resultado = parsear(tokens_por_linha, gramatica["tabela"])

    salvarTokens(tokens_por_linha, "output/tokens_saida.txt")
    salvar_resultado_parser(resultado, "output/parser_resultado.txt")

    print(f"ACEITO: {resultado['aceito']}")

    if not resultado["aceito"]:
        salvar_gramatica_markdown(gramatica, "docs/gramatica_ll1.md")
        return

    arvore = gerarArvore(resultado)
    salvarArvoreJSON(arvore, "output/arvore.json")
    salvarArvoreTexto(arvore, "output/arvore.txt")

    codigo = gerarAssembly(arvore)
    salvar_assembly(codigo, "output/programa.s")
    salvar_gramatica_com_arvore(gramatica, arvore, "docs/gramatica_ll1.md")

if __name__ == "__main__":
    main()