# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

import subprocess
import sys
import os


ARQUIVOS_VALIDOS = [
    "teste1.txt",
    "teste2.txt",
    "teste3.txt",
]

ARQUIVOS_INVALIDOS = [
    ("teste_invalido.txt",        "erro sintatico"),
    ("teste_lexico_invalido.txt", "erro lexico"),
]


def rodar(arquivo):
    resultado = subprocess.run(
        [sys.executable, "main.py", arquivo],
        capture_output=True,
        text=True,
    )
    saida = resultado.stdout
    return "ACEITO: True" in saida, saida


def main():
    total = 0
    sucessos = 0

    print("Testes que devem ser ACEITOS:\n")
    for arquivo in ARQUIVOS_VALIDOS:
        total += 1
        if not os.path.isfile(arquivo):
            print(f"  [AUSENTE] {arquivo}")
            continue
        aceito, _ = rodar(arquivo)
        if aceito:
            print(f"  [OK]     {arquivo}")
            sucessos += 1
        else:
            print(f"  [FALHOU] {arquivo} (esperava ACEITO, veio REJEITADO)")

    print("\nTestes que devem ser REJEITADOS:\n")
    for arquivo, motivo in ARQUIVOS_INVALIDOS:
        total += 1
        if not os.path.isfile(arquivo):
            print(f"  [AUSENTE] {arquivo}")
            continue
        aceito, _ = rodar(arquivo)
        if not aceito:
            print(f"  [OK]     {arquivo} ({motivo})")
            sucessos += 1
        else:
            print(f"  [FALHOU] {arquivo} (esperava REJEITADO, veio ACEITO)")

    print(f"\nResumo: {sucessos}/{total} testes com o resultado esperado.")


if __name__ == "__main__":
    main()
