# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

import json
import os

def gerarArvore(resultado_parser):
    if not resultado_parser["aceito"]:
        raise ValueError("Nao e possivel gerar arvore de um programa rejeitado")
    return resultado_parser["arvore"]

def noParaDict(no):
    tipo = no["tipo"]

    if tipo == "numero":
        return {"tipo": tipo, "valor": no["valor"]}

    if tipo == "carregar_memoria":
        return {"tipo": tipo, "nome": no["nome"]}

    if tipo == "carregar_resultado":
        return {"tipo": tipo, "indice": no["indice"]}

    if tipo == "gravar_memoria":
        return {
            "tipo": tipo,
            "nome": no["nome"],
            "valor": noParaDict(no["valor"]),
        }

    if tipo in ("binaria", "relacional"):
        return {
            "tipo": tipo,
            "operador": no["operador"],
            "esquerda": noParaDict(no["esquerda"]),
            "direita": noParaDict(no["direita"]),
        }

    if tipo == "expressao":
        return {
            "tipo": "expressao",
            "linha": no["linha"],
            "fonte": no["fonte"],
            "estrutura": noParaDict(no["estrutura"]),
        }

    if tipo == "if":
        return {
            "tipo": "if",
            "linha": no.get("linha"),
            "fonte": no.get("fonte"),
            "condicao": noParaDict(no["condicao"]),
            "bloco_then": [noParaDict(x) for x in no["bloco_then"]],
            "bloco_else": (
                None if no["bloco_else"] is None
                else [noParaDict(x) for x in no["bloco_else"]]
            ),
        }

    if tipo == "while":
        return {
            "tipo": "while",
            "linha": no.get("linha"),
            "fonte": no.get("fonte"),
            "condicao": noParaDict(no["condicao"]),
            "bloco": [noParaDict(x) for x in no["bloco"]],
        }

    if tipo == "programa":
        return {
            "tipo": "programa",
            "linha_inicio": no["linha_inicio"],
            "linha_fim": no["linha_fim"],
            "comandos": [noParaDict(x) for x in no["comandos"]],
        }

    raise ValueError(f"Tipo de no desconhecido ao serializar: {tipo}")

def salvarArvoreJSON(arvore, caminho_saida):
    pasta = os.path.dirname(caminho_saida)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(noParaDict(arvore), arquivo, indent=2, ensure_ascii=False)