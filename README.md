# Fase 2 - Analisador Sintático LL(1)

## Informações Institucionais

- Instituição: PUCPR
- Ano: 2026
- Disciplina: Linguagens Formais e Compiladores
- Curso: Engenharia de Computação
- Turma / Semestre: 9º período — 2026-1
- Professor: Frank Coelho de Alcantara
- Fase do Projeto: Fase 2 — Analisador Sintático LL(1)
- Grupo (Canvas): RA2 17
- Integrantes (ordem alfabética):
  - Eduardo Hideo Itinoseke Ogassawara — GitHub: hiduard
  - Gabriel Barbosa Fernandes de Oliveira — GitHub: GabrielBarbosaFernandes

---

## Objetivo do Projeto

Este projeto implementa a Fase 2 do trabalho prático da disciplina, com foco na construção de um analisador sintático LL(1) para uma linguagem simplificada em notação polonesa reversa (RPN).

O sistema é capaz de:

- ler um arquivo de texto contendo um programa escrito na linguagem definida;
- realizar a análise léxica por autômato finito determinístico (sem regex), produzindo um vetor de tokens;
- construir a gramática LL(1) com todas as regras de produção, derivando diretamente sobre os tokens individuais gerados pelo léxico;
- calcular os conjuntos FIRST e FOLLOW para cada não-terminal;
- montar a tabela de análise LL(1) e verificar a ausência de conflitos;
- validar a estrutura sintática do programa com parser descendente recursivo, uma função por não-terminal;
- gerar a árvore sintática estruturada durante o parsing, em formato JSON e texto;
- gerar código Assembly ARMv7 a partir da árvore, compatível com o simulador CPUlator ARMv7 DEC1-SOC(v16.1).

---

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa é necessária (`sys`, `os`, `json` são da biblioteca padrão)

---

## Como Compilar e Executar

O programa não requer compilação. O ponto de entrada único é `main.py`, que aceita apenas o nome do arquivo de entrada como parâmetro (conforme exigido pelo enunciado — sem menu, sem interação):

```bash
python main.py <arquivo_de_entrada>
```

Exemplos:

```bash
python main.py teste1.txt
python main.py teste2.txt
python main.py teste3.txt
python main.py teste_invalido.txt
python main.py teste_lexico_invalido.txt
```

Para rodar a suíte completa de testes de uma vez:

```bash
python rodar_todos_testes.py
```

### Formato da entrada

- Arquivos `.txt`: código-fonte da linguagem (análise léxica é feita automaticamente).
- Arquivos `.tok` ou `.tokens`: tokens pré-gerados pela Fase 1, no formato gerado por `utils.salvarTokens`.

Isso atende à exigência do enunciado de que o parser seja capaz de consumir o string de tokens da Fase 1 (`lerTokens(arquivo)` em `utils.py`).

### Arquivos gerados automaticamente

Após cada execução, os seguintes arquivos são criados ou atualizados:

| Arquivo | Conteúdo |
|---------|----------|
| `output/tokens_saida.txt` | Tokens gerados pela análise léxica |
| `output/parser_resultado.txt` | Resultado do parser (aceitação ou erro) com todas as derivações LL(1) aplicadas |
| `output/arvore.json` | Árvore sintática em formato JSON |
| `output/arvore.txt` | Árvore sintática em formato texto indentado |
| `output/programa.s` | Código Assembly ARMv7 gerado a partir da árvore |
| `docs/gramatica_ll1.md` | Gramática completa, FIRST, FOLLOW, tabela LL(1) e a árvore sintática do último teste executado |

---

## Como Depurar

Para inspecionar o resultado do parser e a árvore gerada:

```bash
python main.py teste1.txt
cat output/arvore.txt
cat output/parser_resultado.txt
cat output/programa.s
cat docs/gramatica_ll1.md
```

Para verificar o comportamento em programas rejeitados:

```bash
python main.py teste_invalido.txt          # erro sintático: (ENDIF) solto
python main.py teste_lexico_invalido.txt   # vários erros léxicos em sequência
```

Em caso de erro, `output/parser_resultado.txt` contém a mensagem do erro encontrado (com número da linha e trecho original) e a lista das derivações aplicadas até o ponto do erro — útil para entender onde o parser travou.

Rodar com `python -u` força o `stdout` sem buffer, facilitando acompanhar a execução em tempo real:

```bash
python -u main.py teste2.txt
```

---

## Como validar o Assembly no CPUlator

1. Execute `python main.py teste1.txt` (ou teste2, teste3).
2. Abra o CPUlator em https://cpulator.01xz.net/?sys=arm-de1soc.
3. Copie o conteúdo de `output/programa.s` e cole no editor do CPUlator.
4. Clique em Compile and Load (ou tecle F5).
5. Clique em Continue para executar. O programa termina em um loop `fim: b fim` (intencional).
6. No painel Memory, procure os símbolos `MEM_<nome>` e `RESULTADO_<linha>` para conferir os valores finais.
7. Exemplo de verificação para `teste1.txt`:
   - `MEM_X` deve terminar em `0.0` (laço decrementa X de 10 até 0)
   - `MEM_SOMA` deve ser `30.0` (X + Y = 10.0 + 20.0, antes do loop)
   - `MEM_DOBRO` deve ser `60.0`
   - `MEM_SAIDA` deve ser `0.0` (inicialmente X=10 > Y=20 é falso → ELSE)

Para cada um dos testes válidos (`teste1.txt`, `teste2.txt`, `teste3.txt`), gere o Assembly e valide no CPUlator. Os valores finais nas memórias são o critério de correção funcional.

### Validação realizada

O grupo executou o Assembly de `teste1.txt` no CPUlator ARMv7 DEC1-SOC(v16.1) e conferiu que os valores finais das memórias batem com o esperado. O screenshot da execução está em `docs/cpulator_teste1.png`.

Resumo dos valores verificados na execução de `teste1.txt`:

| Símbolo | Esperado | Obtido |
|---|---|---|
| `MEM_X` | `0.0` | ✓ |
| `MEM_Y` | `20.0` | ✓ |
| `MEM_SOMA` | `30.0` | ✓ |
| `MEM_DOBRO` | `60.0` | ✓ |
| `MEM_MEDIA` | `15.0` | ✓ |
| `MEM_SAIDA` | `0.0` | ✓ |

---



## Estrutura do Repositório

```
.
├── main.py                        # Ponto de entrada (argv[1] = arquivo de entrada)
├── tokens.py                      # Constantes de tipos de tokens
├── lexico.py                      # Analisador léxico (AFD por funções, sem regex)
├── leitor.py                      # Leitura do arquivo preservando número de linha
├── utils.py                       # lerTokens / salvarTokens (integração Fase 1)
├── gramatica.py                   # construirGramatica + FIRST/FOLLOW/tabela
├── parser_ll1.py                  # Parser descendente recursivo LL(1)
├── arvore.py                      # Serialização da árvore sintática
├── assembly.py                    # Gerador de código ARMv7
├── rodar_todos_testes.py          # Script auxiliar: executa toda a suíte
├── teste1.txt                     # Teste válido: todas operações + IF + WHILE
├── teste2.txt                     # Teste válido: aninhamento IF-dentro-de-WHILE
├── teste3.txt                     # Teste válido: memórias + RES + controles
├── teste_invalido.txt             # Erros sintáticos variados
├── teste_lexico_invalido.txt      # Erros léxicos variados
├── docs/
│   └── gramatica_ll1.md           # Gramática, FIRST, FOLLOW, tabela, árvore do último teste
└── output/
    ├── tokens_saida.txt
    ├── parser_resultado.txt
    ├── arvore.json
    ├── arvore.txt
    └── programa.s
```

---

## Estrutura Geral da Linguagem

Todo programa deve começar com `(START)` e terminar com `(END)`. As expressões seguem a notação polonesa reversa (RPN) no formato `(A B op)`.

### Operadores suportados

| Operador | Operação | Exemplo |
|----------|----------|---------|
| `+` | Adição | `(A B +)` |
| `-` | Subtração | `(A B -)` |
| `*` | Multiplicação | `(A B *)` |
| `\|` | Divisão real (double) | `(A B \|)` |
| `/` | Divisão inteira | `(A B /)` |
| `%` | Resto da divisão inteira | `(A B %)` |
| `^` | Potenciação (expoente inteiro positivo) | `(A B ^)` |

### Comandos especiais

| Sintaxe | Significado |
|---------|-------------|
| `(N RES)` | Carrega o resultado da expressão N linhas anteriores |
| `(V MEM)` | Grava o valor V na memória chamada MEM |
| `(MEM)` | Carrega o valor armazenado em MEM (retorna 0 se não inicializada) |

`MEM` pode ser qualquer sequência de letras latinas maiúsculas (ex: `X`, `VAR`, `SOMA`, `CONTADOR`).

### Expressões aninhadas

Expressões podem ser aninhadas sem limite definido:

```
(A (C D *) +)          @ soma A com o produto de C e D
((A B %) (D E *) /)    @ divide o resto de A/B pelo produto D*E
```

---

## Sintaxe das Estruturas de Controle

A sintaxe foi definida pelo grupo para manter o padrão da linguagem: tudo entre parênteses, operador ao final, lógica RPN.

### Operadores relacionais disponíveis

`>`, `<`, `>=`, `<=`, `==`, `!=`

### Estrutura condicional (IF / ELSE / ENDIF)

```
(A B > IF)
(comando_verdadeiro)
(ELSE)
(comando_falso)
(ENDIF)
```

O `(ELSE)` é opcional:

```
(A B > IF)
(comando_verdadeiro)
(ENDIF)
```

Regras:
- A condição deve ser uma expressão relacional em RPN: `(operando_esq operando_dir operador_rel IF)`
- Os operandos podem ser números, memórias ou sub-expressões entre parênteses
- O bloco THEN pode conter qualquer número de comandos, incluindo IFs e WHILEs aninhados
- O bloco ELSE também pode conter estruturas aninhadas

### Estrutura de repetição (WHILE / ENDWHILE)

```
(A B < WHILE)
(corpo_do_laco)
(ENDWHILE)
```

Regras:
- A condição é reavaliada a cada iteração
- O bloco pode conter qualquer número de comandos, incluindo IFs e WHILEs aninhados
- O laço termina quando a condição relacional for falsa

### Exemplo completo com aninhamento

```
(START)
(10.0 X)
(1.0 PASSO)
((X) 0.0 > WHILE)
(((X) (PASSO) -) X)
((X) 5.0 == IF)
(99.0 FLAG)
(ELSE)
(0.0 FLAG)
(ENDIF)
(ENDWHILE)
(X)
(END)
```

---

## Decisões de Projeto

### Gramática LL(1) no nível de tokens

A gramática LL(1) deriva diretamente sobre o vetor de tokens gerado pelo analisador léxico (tokens individuais: `LPAREN`, `RPAREN`, `NUMBER`, `MEMORY`, `OPERATOR`, `REL_OP`, `RES`, `START`, `END`, `IF`, `ELSE`, `ENDIF`, `WHILE`, `ENDWHILE`). Ela cobre a estrutura geral do programa, expressões RPN em qualquer nível de aninhamento, comandos especiais (RES, MEM, gravação), e estruturas de controle IF/ELSE/ENDIF e WHILE/ENDWHILE — conforme exigido pela seção 3.1 do enunciado.

A árvore sintática é construída durante o parsing (cada método `parse_<nao_terminal>` do parser devolve um fragmento da árvore), não em uma etapa posterior.

### Fatoração léxica de LPAREN

Para manter a gramática em LL(1) puro (lookahead de 1 token) sem precisar simular lookahead-2 em tempo de parsing, o token `LPAREN` é promovido em cinco classes distintas, antes do parser iniciar, conforme o token imediatamente seguinte:

| Classe | Contexto |
|---|---|
| `LPAREN_CMD` | `(` que inicia um comando ou expressão |
| `LPAREN_END` | `(` imediatamente antes de `END` |
| `LPAREN_ELSE` | `(` imediatamente antes de `ELSE` |
| `LPAREN_ENDIF` | `(` imediatamente antes de `ENDIF` |
| `LPAREN_ENDWHILE` | `(` imediatamente antes de `ENDWHILE` |

Essa promoção é feita pela função `promoverLParens` em `parser_ll1.py` e é equivalente a usar terminais distintos na gramática. Sem essa fatoração, a tabela LL(1) teria conflito no não-terminal `fim_if` (ambas as alternativas começariam com `LPAREN`); com ela, a tabela LL(1) tem zero conflitos, como pode ser verificado no markdown `docs/gramatica_ll1.md` (seção "Conflitos").

### Ponto flutuante no Assembly

Todos os valores são tratados internamente como `double` (IEEE 754 de 64 bits) usando os registradores VFP do ARMv7 (`d0`–`d2`). As operações de divisão inteira e resto convertem os operandos para inteiro via `vcvt`, realizam a operação com registradores inteiros (por subtração repetida, para manter compatibilidade com o DEC1-SOC que não possui `sdiv`), e convertem o resultado de volta para `double`. O sinal do resultado é calculado via XOR dos sinais dos operandos.

### Potenciação

A potenciação `(A B ^)` é implementada por um loop de multiplicação em Assembly, pois ARMv7 não possui instrução nativa de potenciação. O expoente é tratado como inteiro positivo. Para expoente ≤ 0, o resultado é 1.0.

### RES e linha de referência

`(N RES)` acessa o resultado salvo da expressão N linhas antes da linha atual. Cada linha de expressão salva seu resultado em `RESULTADO_<numero_da_linha>` na seção `.data`. O valor `N=0` é rejeitado pois referenciaria a linha atual (ainda não calculada).

### Divisão por zero

Em divisões (inteira ou real), o divisor zero produz resultado zero em vez de interromper a execução — escolha feita para manter o programa Assembly robusto no simulador.

---

## Cobertura dos testes

### Testes válidos (devem ser ACEITOS)

| Arquivo | Linhas | Cobertura |
|---|---|---|
| `teste1.txt` | 21 | Todas as operações, RES, gravação e leitura de memória, IF/ELSE/ENDIF, WHILE/ENDWHILE |
| `teste2.txt` | 26 | IF-dentro-de-WHILE-dentro-de-IF, múltiplas memórias, operações encadeadas |
| `teste3.txt` | 22 | Expressões aninhadas profundas, IF simples, WHILE com corpo modificador |

### Testes inválidos (devem ser REJEITADOS)

| Arquivo | Linhas | Erros cobertos |
|---|---|---|
| `teste_invalido.txt` | 11 | `ENDIF` solto, `ELSE` solto, `ENDWHILE` solto, `WHILE` sem `ENDWHILE` |
| `teste_lexico_invalido.txt` | 12 | Números malformados (`3.14.5`, `3.`, `.5`), caracteres inválidos (`&`, `=`, `!`, `@`, `#`), operador obsoleto (`//`), minúsculas (`abc`) |

Para rodar todos os testes em sequência:

```bash
python rodar_todos_testes.py
```

Saída esperada: `5/5 testes com o resultado esperado.`
