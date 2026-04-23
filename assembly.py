# Integrantes do grupo (ordem alfabética):
# Eduardo Hideo Itinoseke Ogassawara - hiduard
# Gabriel Barbosa Fernandes de Oliveira - GabrielBarbosaFernandes
#
# Nome do grupo no Canvas: RA2 17

def gerarRotuloConstante(valor):
    rotulo = valor.replace("-", "NEG_").replace(".", "_")
    return f"CONST_{rotulo}"


def normalizarLiteralDouble(valor):
    if "." not in valor:
        return valor + ".0"
    return valor


def novoRotulo(ctx, prefixo, linha):
    ctx["contador_rotulos"] += 1
    return f"{prefixo}_{linha}_{ctx['contador_rotulos']}"

def coletarConstantesExpressao(no, constantes):
    tipo = no["tipo"]

    if tipo == "numero":
        constantes.add(normalizarLiteralDouble(no["valor"]))
        return

    if tipo in ("carregar_memoria", "carregar_resultado"):
        return

    if tipo == "gravar_memoria":
        coletarConstantesExpressao(no["valor"], constantes)
        return

    if tipo in ("binaria", "relacional"):
        coletarConstantesExpressao(no["esquerda"], constantes)
        coletarConstantesExpressao(no["direita"], constantes)
        return


def coletarMemoriasExpressao(no, memorias):
    tipo = no["tipo"]

    if tipo == "carregar_memoria":
        memorias.add(no["nome"])
        return

    if tipo == "gravar_memoria":
        memorias.add(no["nome"])
        coletarMemoriasExpressao(no["valor"], memorias)
        return

    if tipo in ("binaria", "relacional"):
        coletarMemoriasExpressao(no["esquerda"], memorias)
        coletarMemoriasExpressao(no["direita"], memorias)
        return

    if tipo in ("numero", "carregar_resultado"):
        return


def coletarComando(comando, constantes, memorias):
    tipo = comando["tipo"]

    if tipo == "expressao":
        coletarConstantesExpressao(comando["estrutura"], constantes)
        coletarMemoriasExpressao(comando["estrutura"], memorias)
        return

    if tipo == "if":
        coletarConstantesExpressao(comando["condicao"], constantes)
        coletarMemoriasExpressao(comando["condicao"], memorias)
        for item in comando["bloco_then"]:
            coletarComando(item, constantes, memorias)
        if comando["bloco_else"] is not None:
            for item in comando["bloco_else"]:
                coletarComando(item, constantes, memorias)
        return

    if tipo == "while":
        coletarConstantesExpressao(comando["condicao"], constantes)
        coletarMemoriasExpressao(comando["condicao"], memorias)
        for item in comando["bloco"]:
            coletarComando(item, constantes, memorias)
        return


def coletarPrograma(arvore, constantes, memorias):
    for comando in arvore["comandos"]:
        coletarComando(comando, constantes, memorias)

def gerarSecaoDados(arvore):
    linhas = [".data"]

    constantes = {"0.0", "1.0"}
    memorias = set()

    coletarPrograma(arvore, constantes, memorias)

    for valor in sorted(constantes):
        rotulo = gerarRotuloConstante(valor)
        literal = normalizarLiteralDouble(valor)
        linhas.append(f"{rotulo}: .double {literal}")

    for nome in sorted(memorias):
        linhas.append(f"MEM_{nome}: .double 0.0")

    for numero_linha in range(1, arvore["linha_fim"] + 1):
        linhas.append(f"RESULTADO_{numero_linha}: .double 0.0")

    return linhas

def gerarCodigoNumero(no):
    valor = normalizarLiteralDouble(no["valor"])
    rotulo = gerarRotuloConstante(valor)
    return [
        f"    ldr r0, ={rotulo}",
        "    vldr d0, [r0]",
    ]


def gerarCodigoCarregarMemoria(no):
    nome = no["nome"]
    return [
        f"    ldr r0, =MEM_{nome}",
        "    vldr d0, [r0]",
    ]


def gerarInstrucaoOperador(operador):
    if operador == "+":
        return "    vadd.f64 d0, d1, d0"
    if operador == "-":
        return "    vsub.f64 d0, d1, d0"
    if operador == "*":
        return "    vmul.f64 d0, d1, d0"
    if operador == "|":
        return "    vdiv.f64 d0, d1, d0"
    return None

def gerarCodigoNo(no, linha_atual, ctx):
    tipo = no["tipo"]

    if tipo == "numero":
        return gerarCodigoNumero(no)

    if tipo == "carregar_memoria":
        return gerarCodigoCarregarMemoria(no)

    if tipo == "gravar_memoria":
        linhas = []
        linhas.extend(gerarCodigoNo(no["valor"], linha_atual, ctx))
        linhas.append(f"    ldr r0, =MEM_{no['nome']}")
        linhas.append("    vstr d0, [r0]")
        return linhas

    if tipo == "carregar_resultado":
        deslocamento = int(no["indice"])

        if deslocamento == 0:
            raise ValueError(
                f"RES 0 invalido na linha {linha_atual}: "
                "nao e possivel referenciar o resultado da linha atual"
            )

        linha_destino = linha_atual - deslocamento

        if linha_destino < 1:
            raise ValueError(
                f"RES {deslocamento} invalido na linha {linha_atual}: "
                f"aponta para linha {linha_destino}, que nao existe"
            )

        return [
            f"    ldr r0, =RESULTADO_{linha_destino}",
            "    vldr d0, [r0]",
        ]
    if tipo == "binaria":
        operador = no["operador"]

        if operador in ["+", "-", "*", "|"]:
            instrucao = gerarInstrucaoOperador(operador)
            linhas = []
            linhas.extend(gerarCodigoNo(no["esquerda"], linha_atual, ctx))
            linhas.append("    vpush {d0}")
            linhas.extend(gerarCodigoNo(no["direita"], linha_atual, ctx))
            linhas.append("    vpop {d1}")
            linhas.append(instrucao)
            return linhas

        raise ValueError(f"Operador binario ainda nao implementado: {operador}")
    raise ValueError(f"No nao suportado ainda: {tipo}")


def gerarCodigoComando(comando, ctx):
    linhas = []
    tipo = comando["tipo"]

    if tipo == "expressao":
        linhas.append("")
        linhas.append(f"    @ Linha {comando['linha']}")
        linhas.append(f"    @ Fonte: {comando['fonte']}")

        codigo = gerarCodigoNo(comando["estrutura"], comando["linha"], ctx)
        linhas.extend(codigo)
        linhas.append(f"    ldr r0, =RESULTADO_{comando['linha']}")
        linhas.append("    vstr d0, [r0]")
        return linhas

    raise ValueError(f"Comando nao suportado ainda: {tipo}")

def gerarAssembly(arvore):
    ctx = {"contador_rotulos": 0}

    linhas = []
    linhas.extend(gerarSecaoDados(arvore))
    linhas.append("")
    linhas.append(".text")
    linhas.append(".global _start")
    linhas.append("_start:")

    for comando in arvore["comandos"]:
        linhas.extend(gerarCodigoComando(comando, ctx))

    linhas.append("")
    linhas.append("fim:")
    linhas.append("    b fim")

    return "\n".join(linhas)