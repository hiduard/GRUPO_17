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

def gerarCodigoDoubleParaInt(reg_double, reg_single, reg_int):
    return [
        f"    vcvt.s32.f64 {reg_single}, {reg_double}",
        f"    vmov {reg_int}, {reg_single}",
    ]


def gerarCodigoIntParaDouble(reg_int, reg_single, reg_double):
    return [
        f"    vmov {reg_single}, {reg_int}",
        f"    vcvt.f64.s32 {reg_double}, {reg_single}",
    ]

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

def gerarCodigoDivisaoInteira(esquerda, direita, linha_atual, ctx):

    lbl_divzero = novoRotulo(ctx, "DIVZERO", linha_atual)
    lbl_loop    = novoRotulo(ctx, "DIV_LOOP", linha_atual)
    lbl_fim     = novoRotulo(ctx, "DIVINT_FIM", linha_atual)
    lbl_neg     = novoRotulo(ctx, "DIVINT_NEG", linha_atual)
    lbl_end     = novoRotulo(ctx, "DIVINT_END", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")
    linhas.extend(direita)
    linhas.append("    vpop {d1}")

    linhas.extend(gerarCodigoDoubleParaInt("d1", "s2", "r4"))
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r5"))

    linhas.append("    cmp r5, #0")
    linhas.append(f"    beq {lbl_divzero}")

    linhas.append("    eor r7, r4, r5")

    linhas.append("    cmp r4, #0")
    linhas.append("    rsblt r4, r4, #0")
    linhas.append("    cmp r5, #0")
    linhas.append("    rsblt r5, r5, #0")

    linhas.append("    mov r6, #0")
    linhas.append(f"{lbl_loop}:")
    linhas.append("    cmp r4, r5")
    linhas.append(f"    blt {lbl_fim}")
    linhas.append("    sub r4, r4, r5")
    linhas.append("    add r6, r6, #1")
    linhas.append(f"    b {lbl_loop}")

    linhas.append(f"{lbl_divzero}:")
    linhas.append("    mov r6, #0")
    linhas.append(f"    b {lbl_end}")

    linhas.append(f"{lbl_fim}:")
    linhas.append("    cmp r7, #0")
    linhas.append(f"    bge {lbl_end}")
    linhas.append(f"    b {lbl_neg}")
    linhas.append(f"{lbl_neg}:")
    linhas.append("    rsb r6, r6, #0")

    linhas.append(f"{lbl_end}:")
    linhas.extend(gerarCodigoIntParaDouble("r6", "s0", "d0"))
    return linhas

def gerarCodigoRestoInteiro(esquerda, direita, linha_atual, ctx):
    lbl_divzero = novoRotulo(ctx, "RESTO_DIVZERO", linha_atual)
    lbl_loop    = novoRotulo(ctx, "RESTO_LOOP", linha_atual)
    lbl_fim     = novoRotulo(ctx, "RESTO_FIM", linha_atual)
    lbl_neg     = novoRotulo(ctx, "RESTO_NEG", linha_atual)
    lbl_end     = novoRotulo(ctx, "RESTO_END", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")
    linhas.extend(direita)
    linhas.append("    vpop {d1}")

    linhas.extend(gerarCodigoDoubleParaInt("d1", "s2", "r4"))
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r5"))

    linhas.append("    cmp r5, #0")
    linhas.append(f"    beq {lbl_divzero}")

    linhas.append("    mov r7, r4")

    linhas.append("    cmp r4, #0")
    linhas.append("    rsblt r4, r4, #0")
    linhas.append("    cmp r5, #0")
    linhas.append("    rsblt r5, r5, #0")

    linhas.append(f"{lbl_loop}:")
    linhas.append("    cmp r4, r5")
    linhas.append(f"    blt {lbl_fim}")
    linhas.append("    sub r4, r4, r5")
    linhas.append(f"    b {lbl_loop}")

    linhas.append(f"{lbl_divzero}:")
    linhas.append("    mov r4, #0")
    linhas.append(f"    b {lbl_end}")

    linhas.append(f"{lbl_fim}:")
    linhas.append("    cmp r7, #0")
    linhas.append(f"    bge {lbl_end}")
    linhas.append(f"    b {lbl_neg}")
    linhas.append(f"{lbl_neg}:")
    linhas.append("    rsb r4, r4, #0")

    linhas.append(f"{lbl_end}:")
    linhas.extend(gerarCodigoIntParaDouble("r4", "s0", "d0"))
    return linhas

def gerarCodigoPotencia(esquerda, direita, linha_atual, ctx):
    lbl_loop = novoRotulo(ctx, "POT_LOOP", linha_atual)
    lbl_fim  = novoRotulo(ctx, "POT_FIM", linha_atual)

    linhas = []

    linhas.extend(esquerda)
    linhas.append("    vpush {d0}")         

    linhas.extend(direita)
    linhas.extend(gerarCodigoDoubleParaInt("d0", "s0", "r4"))  

    linhas.append("    vpop {d2}")           
    linhas.append("    ldr r0, =CONST_1_0")
    linhas.append("    vldr d0, [r0]")       

    linhas.append("    cmp r4, #0")
    linhas.append(f"    ble {lbl_fim}")       

    linhas.append(f"{lbl_loop}:")
    linhas.append("    vmul.f64 d0, d0, d2")
    linhas.append("    subs r4, r4, #1")
    linhas.append(f"    bne {lbl_loop}")

    linhas.append(f"{lbl_fim}:")
    return linhas

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
        
        if operador == "/":
            return gerarCodigoDivisaoInteira(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )

        if operador == "%":
            return gerarCodigoRestoInteiro(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )
        
        if operador == "^":
            return gerarCodigoPotencia(
                gerarCodigoNo(no["esquerda"], linha_atual, ctx),
                gerarCodigoNo(no["direita"], linha_atual, ctx),
                linha_atual,
                ctx,
            )
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