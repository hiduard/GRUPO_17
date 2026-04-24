# Gramatica LL(1)

## Simbolo inicial

`programa`

## Producoes

Notacao EBNF: **nao-terminais em minusculas**, **TERMINAIS EM MAIUSCULAS**.

- `programa -> abre_start lista_prog fecha_end`
- `abre_start -> LPAREN_CMD START RPAREN`
- `fecha_end -> LPAREN_END END RPAREN`
- `lista_prog -> comando lista_prog`
- `lista_prog -> epsilon`
- `lista_if -> comando lista_if`
- `lista_if -> epsilon`
- `lista_while -> comando lista_while`
- `lista_while -> epsilon`
- `comando -> LPAREN_CMD interior`
- `interior -> NUMBER apos_num`
- `interior -> MEMORY apos_mem`
- `interior -> LPAREN_CMD sub apos_sub`
- `apos_num -> RES RPAREN`
- `apos_num -> NUMBER resto_num`
- `apos_num -> MEMORY resto_mem_grava`
- `apos_num -> LPAREN_CMD sub resto_sub`
- `apos_mem -> RPAREN`
- `apos_mem -> NUMBER resto_num`
- `apos_mem -> MEMORY resto_mem_grava`
- `apos_mem -> LPAREN_CMD sub resto_sub`
- `apos_sub -> RPAREN`
- `apos_sub -> NUMBER resto_num`
- `apos_sub -> MEMORY resto_mem_grava`
- `apos_sub -> LPAREN_CMD sub resto_sub`
- `resto_num -> OPERATOR RPAREN`
- `resto_num -> REL_OP cauda_rel`
- `resto_mem_grava -> RPAREN`
- `resto_mem_grava -> OPERATOR RPAREN`
- `resto_mem_grava -> REL_OP cauda_rel`
- `resto_sub -> OPERATOR RPAREN`
- `resto_sub -> REL_OP cauda_rel`
- `cauda_rel -> RPAREN`
- `cauda_rel -> IF RPAREN lista_if fim_if`
- `cauda_rel -> WHILE RPAREN lista_while abre_endwhile`
- `fim_if -> abre_else lista_if abre_endif`
- `fim_if -> abre_endif`
- `abre_else -> LPAREN_ELSE ELSE RPAREN`
- `abre_endif -> LPAREN_ENDIF ENDIF RPAREN`
- `abre_endwhile -> LPAREN_ENDWHILE ENDWHILE RPAREN`
- `sub -> NUMBER apos_num_sub`
- `sub -> MEMORY apos_mem_sub`
- `sub -> LPAREN_CMD sub apos_sub_sub`
- `apos_num_sub -> RES RPAREN`
- `apos_num_sub -> NUMBER resto_num_sub`
- `apos_num_sub -> MEMORY resto_mem_grava_sub`
- `apos_num_sub -> LPAREN_CMD sub resto_sub_sub`
- `apos_mem_sub -> RPAREN`
- `apos_mem_sub -> NUMBER resto_num_sub`
- `apos_mem_sub -> MEMORY resto_mem_grava_sub`
- `apos_mem_sub -> LPAREN_CMD sub resto_sub_sub`
- `apos_sub_sub -> RPAREN`
- `apos_sub_sub -> NUMBER resto_num_sub`
- `apos_sub_sub -> MEMORY resto_mem_grava_sub`
- `apos_sub_sub -> LPAREN_CMD sub resto_sub_sub`
- `resto_num_sub -> OPERATOR RPAREN`
- `resto_num_sub -> REL_OP RPAREN`
- `resto_mem_grava_sub -> RPAREN`
- `resto_mem_grava_sub -> OPERATOR RPAREN`
- `resto_mem_grava_sub -> REL_OP RPAREN`
- `resto_sub_sub -> OPERATOR RPAREN`
- `resto_sub_sub -> REL_OP RPAREN`

## FIRST

- `FIRST(abre_else) = { LPAREN_ELSE }`
- `FIRST(abre_endif) = { LPAREN_ENDIF }`
- `FIRST(abre_endwhile) = { LPAREN_ENDWHILE }`
- `FIRST(abre_start) = { LPAREN_CMD }`
- `FIRST(apos_mem) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(apos_mem_sub) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(apos_num) = { LPAREN_CMD, MEMORY, NUMBER, RES }`
- `FIRST(apos_num_sub) = { LPAREN_CMD, MEMORY, NUMBER, RES }`
- `FIRST(apos_sub) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(apos_sub_sub) = { LPAREN_CMD, MEMORY, NUMBER, RPAREN }`
- `FIRST(cauda_rel) = { IF, RPAREN, WHILE }`
- `FIRST(comando) = { LPAREN_CMD }`
- `FIRST(fecha_end) = { LPAREN_END }`
- `FIRST(fim_if) = { LPAREN_ELSE, LPAREN_ENDIF }`
- `FIRST(interior) = { LPAREN_CMD, MEMORY, NUMBER }`
- `FIRST(lista_if) = { LPAREN_CMD, epsilon }`
- `FIRST(lista_prog) = { LPAREN_CMD, epsilon }`
- `FIRST(lista_while) = { LPAREN_CMD, epsilon }`
- `FIRST(programa) = { LPAREN_CMD }`
- `FIRST(resto_mem_grava) = { OPERATOR, REL_OP, RPAREN }`
- `FIRST(resto_mem_grava_sub) = { OPERATOR, REL_OP, RPAREN }`
- `FIRST(resto_num) = { OPERATOR, REL_OP }`
- `FIRST(resto_num_sub) = { OPERATOR, REL_OP }`
- `FIRST(resto_sub) = { OPERATOR, REL_OP }`
- `FIRST(resto_sub_sub) = { OPERATOR, REL_OP }`
- `FIRST(sub) = { LPAREN_CMD, MEMORY, NUMBER }`

## FOLLOW

- `FOLLOW(abre_else) = { LPAREN_CMD, LPAREN_ENDIF }`
- `FOLLOW(abre_endif) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(abre_endwhile) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(abre_start) = { LPAREN_CMD, LPAREN_END }`
- `FOLLOW(apos_mem) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_mem_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(apos_num) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_num_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(apos_sub) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(apos_sub_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(cauda_rel) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(comando) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(fecha_end) = { $ }`
- `FOLLOW(fim_if) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(interior) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(lista_if) = { LPAREN_ELSE, LPAREN_ENDIF }`
- `FOLLOW(lista_prog) = { LPAREN_END }`
- `FOLLOW(lista_while) = { LPAREN_ENDWHILE }`
- `FOLLOW(programa) = { $ }`
- `FOLLOW(resto_mem_grava) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_mem_grava_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(resto_num) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_num_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(resto_sub) = { LPAREN_CMD, LPAREN_ELSE, LPAREN_END, LPAREN_ENDIF, LPAREN_ENDWHILE }`
- `FOLLOW(resto_sub_sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`
- `FOLLOW(sub) = { LPAREN_CMD, MEMORY, NUMBER, OPERATOR, REL_OP, RPAREN }`

## Tabela LL(1)

### abre_else

- `[abre_else, LPAREN_ELSE] -> LPAREN_ELSE ELSE RPAREN`

### abre_endif

- `[abre_endif, LPAREN_ENDIF] -> LPAREN_ENDIF ENDIF RPAREN`

### abre_endwhile

- `[abre_endwhile, LPAREN_ENDWHILE] -> LPAREN_ENDWHILE ENDWHILE RPAREN`

### abre_start

- `[abre_start, LPAREN_CMD] -> LPAREN_CMD START RPAREN`

### apos_mem

- `[apos_mem, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_mem, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_mem, NUMBER] -> NUMBER resto_num`
- `[apos_mem, RPAREN] -> RPAREN`

### apos_mem_sub

- `[apos_mem_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_mem_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_mem_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_mem_sub, RPAREN] -> RPAREN`

### apos_num

- `[apos_num, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_num, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_num, NUMBER] -> NUMBER resto_num`
- `[apos_num, RES] -> RES RPAREN`

### apos_num_sub

- `[apos_num_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_num_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_num_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_num_sub, RES] -> RES RPAREN`

### apos_sub

- `[apos_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub`
- `[apos_sub, MEMORY] -> MEMORY resto_mem_grava`
- `[apos_sub, NUMBER] -> NUMBER resto_num`
- `[apos_sub, RPAREN] -> RPAREN`

### apos_sub_sub

- `[apos_sub_sub, LPAREN_CMD] -> LPAREN_CMD sub resto_sub_sub`
- `[apos_sub_sub, MEMORY] -> MEMORY resto_mem_grava_sub`
- `[apos_sub_sub, NUMBER] -> NUMBER resto_num_sub`
- `[apos_sub_sub, RPAREN] -> RPAREN`

### cauda_rel

- `[cauda_rel, IF] -> IF RPAREN lista_if fim_if`
- `[cauda_rel, RPAREN] -> RPAREN`
- `[cauda_rel, WHILE] -> WHILE RPAREN lista_while abre_endwhile`

### comando

- `[comando, LPAREN_CMD] -> LPAREN_CMD interior`

### fecha_end

- `[fecha_end, LPAREN_END] -> LPAREN_END END RPAREN`

### fim_if

- `[fim_if, LPAREN_ELSE] -> abre_else lista_if abre_endif`
- `[fim_if, LPAREN_ENDIF] -> abre_endif`

### interior

- `[interior, LPAREN_CMD] -> LPAREN_CMD sub apos_sub`
- `[interior, MEMORY] -> MEMORY apos_mem`
- `[interior, NUMBER] -> NUMBER apos_num`

### lista_if

- `[lista_if, LPAREN_CMD] -> comando lista_if`
- `[lista_if, LPAREN_ELSE] -> epsilon`
- `[lista_if, LPAREN_ENDIF] -> epsilon`

### lista_prog

- `[lista_prog, LPAREN_CMD] -> comando lista_prog`
- `[lista_prog, LPAREN_END] -> epsilon`

### lista_while

- `[lista_while, LPAREN_CMD] -> comando lista_while`
- `[lista_while, LPAREN_ENDWHILE] -> epsilon`

### programa

- `[programa, LPAREN_CMD] -> abre_start lista_prog fecha_end`

### resto_mem_grava

- `[resto_mem_grava, OPERATOR] -> OPERATOR RPAREN`
- `[resto_mem_grava, REL_OP] -> REL_OP cauda_rel`
- `[resto_mem_grava, RPAREN] -> RPAREN`

### resto_mem_grava_sub

- `[resto_mem_grava_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_mem_grava_sub, REL_OP] -> REL_OP RPAREN`
- `[resto_mem_grava_sub, RPAREN] -> RPAREN`

### resto_num

- `[resto_num, OPERATOR] -> OPERATOR RPAREN`
- `[resto_num, REL_OP] -> REL_OP cauda_rel`

### resto_num_sub

- `[resto_num_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_num_sub, REL_OP] -> REL_OP RPAREN`

### resto_sub

- `[resto_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_sub, REL_OP] -> REL_OP cauda_rel`

### resto_sub_sub

- `[resto_sub_sub, OPERATOR] -> OPERATOR RPAREN`
- `[resto_sub_sub, REL_OP] -> REL_OP RPAREN`

### sub

- `[sub, LPAREN_CMD] -> LPAREN_CMD sub apos_sub_sub`
- `[sub, MEMORY] -> MEMORY apos_mem_sub`
- `[sub, NUMBER] -> NUMBER apos_num_sub`

## Conflitos

Sem conflitos LL(1).

---

## Arvore Sintatica (ultimo teste)

```
programa [1..21]
  expressao [linha 2]
    gravar_memoria(X)
      numero(10.0)
  expressao [linha 3]
    gravar_memoria(Y)
      numero(20)
  expressao [linha 4]
    gravar_memoria(PI)
      numero(3.5)
  expressao [linha 5]
    gravar_memoria(SOMA)
      binaria(+)
        memoria(X)
        memoria(Y)
  expressao [linha 6]
    gravar_memoria(DOBRO)
      binaria(*)
        memoria(SOMA)
        numero(2.0)
  expressao [linha 7]
    gravar_memoria(MEDIA)
      binaria(|)
        memoria(DOBRO)
        numero(4.0)
  expressao [linha 8]
    gravar_memoria(QUOC)
      binaria(/)
        memoria(DOBRO)
        numero(3)
  expressao [linha 9]
    gravar_memoria(RESTO)
      binaria(%)
        memoria(DOBRO)
        numero(3)
  expressao [linha 10]
    gravar_memoria(POT)
      binaria(^)
        memoria(X)
        numero(2)
  expressao [linha 11]
    gravar_memoria(ULTIMO)
      res(2)
  expressao [linha 12]
    memoria(SOMA)
  if [linha 13]
    condicao:
      relacional(>)
        memoria(X)
        memoria(Y)
    then:
      expressao [linha 14]
        gravar_memoria(SAIDA)
          numero(1)
    else:
      expressao [linha 16]
        gravar_memoria(SAIDA)
          numero(0)
  while [linha 18]
    condicao:
      relacional(>)
        memoria(X)
        numero(0.0)
    bloco:
      expressao [linha 19]
        gravar_memoria(X)
          binaria(-)
            memoria(X)
            numero(1)
```
