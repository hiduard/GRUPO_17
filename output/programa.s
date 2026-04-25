.data
CONST_0_0: .double 0.0
CONST_1_0: .double 1.0
CONST_10_0: .double 10.0
CONST_2_0: .double 2.0
CONST_20_0: .double 20.0
CONST_3_0: .double 3.0
CONST_3_5: .double 3.5
CONST_4_0: .double 4.0
MEM_DOBRO: .double 0.0
MEM_MEDIA: .double 0.0
MEM_PI: .double 0.0
MEM_POT: .double 0.0
MEM_QUOC: .double 0.0
MEM_RESTO: .double 0.0
MEM_SAIDA: .double 0.0
MEM_SOMA: .double 0.0
MEM_ULTIMO: .double 0.0
MEM_X: .double 0.0
MEM_Y: .double 0.0
RESULTADO_1: .double 0.0
RESULTADO_2: .double 0.0
RESULTADO_3: .double 0.0
RESULTADO_4: .double 0.0
RESULTADO_5: .double 0.0
RESULTADO_6: .double 0.0
RESULTADO_7: .double 0.0
RESULTADO_8: .double 0.0
RESULTADO_9: .double 0.0
RESULTADO_10: .double 0.0
RESULTADO_11: .double 0.0
RESULTADO_12: .double 0.0
RESULTADO_13: .double 0.0
RESULTADO_14: .double 0.0
RESULTADO_15: .double 0.0
RESULTADO_16: .double 0.0
RESULTADO_17: .double 0.0
RESULTADO_18: .double 0.0
RESULTADO_19: .double 0.0
RESULTADO_20: .double 0.0
RESULTADO_21: .double 0.0

@ Strings para impressao no JTAG UART
STR_DOBRO: .asciz "DOBRO="
STR_MEDIA: .asciz "MEDIA="
STR_PI: .asciz "PI="
STR_POT: .asciz "POT="
STR_QUOC: .asciz "QUOC="
STR_RESTO: .asciz "RESTO="
STR_SAIDA: .asciz "SAIDA="
STR_SOMA: .asciz "SOMA="
STR_ULTIMO: .asciz "ULTIMO="
STR_X: .asciz "X="
STR_Y: .asciz "Y="
STR_NL: .asciz "\n"
STR_PONTO: .asciz "."
STR_MENOS: .asciz "-"
PRINT_BUF: .space 12

.text
.global _start
_start:

    @ Linha 2
    @ Fonte: (10.0 X)
    ldr r0, =CONST_10_0
    vldr d0, [r0]
    ldr r0, =MEM_X
    vstr d0, [r0]
    ldr r0, =RESULTADO_2
    vstr d0, [r0]

    @ Linha 3
    @ Fonte: (20 Y)
    ldr r0, =CONST_20_0
    vldr d0, [r0]
    ldr r0, =MEM_Y
    vstr d0, [r0]
    ldr r0, =RESULTADO_3
    vstr d0, [r0]

    @ Linha 4
    @ Fonte: (3.5 PI)
    ldr r0, =CONST_3_5
    vldr d0, [r0]
    ldr r0, =MEM_PI
    vstr d0, [r0]
    ldr r0, =RESULTADO_4
    vstr d0, [r0]

    @ Linha 5
    @ Fonte: (((X) (Y) +) SOMA)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vadd.f64 d0, d1, d0
    ldr r0, =MEM_SOMA
    vstr d0, [r0]
    ldr r0, =RESULTADO_5
    vstr d0, [r0]

    @ Linha 6
    @ Fonte: (((SOMA) 2.0 *) DOBRO)
    ldr r0, =MEM_SOMA
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_2_0
    vldr d0, [r0]
    vpop {d1}
    vmul.f64 d0, d1, d0
    ldr r0, =MEM_DOBRO
    vstr d0, [r0]
    ldr r0, =RESULTADO_6
    vstr d0, [r0]

    @ Linha 7
    @ Fonte: (((DOBRO) 4.0 |) MEDIA)
    ldr r0, =MEM_DOBRO
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_4_0
    vldr d0, [r0]
    vpop {d1}
    vdiv.f64 d0, d1, d0
    ldr r0, =MEM_MEDIA
    vstr d0, [r0]
    ldr r0, =RESULTADO_7
    vstr d0, [r0]

    @ Linha 8
    @ Fonte: (((DOBRO) 3 /) QUOC)
    ldr r0, =MEM_DOBRO
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_3_0
    vldr d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r4, s2
    vcvt.s32.f64 s0, d0
    vmov r5, s0
    cmp r5, #0
    beq DIVZERO_8_1
    eor r7, r4, r5
    cmp r4, #0
    rsblt r4, r4, #0
    cmp r5, #0
    rsblt r5, r5, #0
    mov r6, #0
DIV_LOOP_8_2:
    cmp r4, r5
    blt DIVINT_FIM_8_3
    sub r4, r4, r5
    add r6, r6, #1
    b DIV_LOOP_8_2
DIVZERO_8_1:
    mov r6, #0
    b DIVINT_END_8_5
DIVINT_FIM_8_3:
    cmp r7, #0
    bge DIVINT_END_8_5
    b DIVINT_NEG_8_4
DIVINT_NEG_8_4:
    rsb r6, r6, #0
DIVINT_END_8_5:
    vmov s0, r6
    vcvt.f64.s32 d0, s0
    ldr r0, =MEM_QUOC
    vstr d0, [r0]
    ldr r0, =RESULTADO_8
    vstr d0, [r0]

    @ Linha 9
    @ Fonte: (((DOBRO) 3 %) RESTO)
    ldr r0, =MEM_DOBRO
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_3_0
    vldr d0, [r0]
    vpop {d1}
    vcvt.s32.f64 s2, d1
    vmov r4, s2
    vcvt.s32.f64 s0, d0
    vmov r5, s0
    cmp r5, #0
    beq RESTO_DIVZERO_9_6
    mov r7, r4
    cmp r4, #0
    rsblt r4, r4, #0
    cmp r5, #0
    rsblt r5, r5, #0
RESTO_LOOP_9_7:
    cmp r4, r5
    blt RESTO_FIM_9_8
    sub r4, r4, r5
    b RESTO_LOOP_9_7
RESTO_DIVZERO_9_6:
    mov r4, #0
    b RESTO_END_9_10
RESTO_FIM_9_8:
    cmp r7, #0
    bge RESTO_END_9_10
    b RESTO_NEG_9_9
RESTO_NEG_9_9:
    rsb r4, r4, #0
RESTO_END_9_10:
    vmov s0, r4
    vcvt.f64.s32 d0, s0
    ldr r0, =MEM_RESTO
    vstr d0, [r0]
    ldr r0, =RESULTADO_9
    vstr d0, [r0]

    @ Linha 10
    @ Fonte: (((X) 2 ^) POT)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_2_0
    vldr d0, [r0]
    vcvt.s32.f64 s0, d0
    vmov r4, s0
    vpop {d2}
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    cmp r4, #0
    ble POT_FIM_10_12
POT_LOOP_10_11:
    vmul.f64 d0, d0, d2
    subs r4, r4, #1
    bne POT_LOOP_10_11
POT_FIM_10_12:
    ldr r0, =MEM_POT
    vstr d0, [r0]
    ldr r0, =RESULTADO_10
    vstr d0, [r0]

    @ Linha 11
    @ Fonte: ((2 RES) ULTIMO)
    ldr r0, =RESULTADO_9
    vldr d0, [r0]
    ldr r0, =MEM_ULTIMO
    vstr d0, [r0]
    ldr r0, =RESULTADO_11
    vstr d0, [r0]

    @ Linha 12
    @ Fonte: (SOMA)
    ldr r0, =MEM_SOMA
    vldr d0, [r0]
    ldr r0, =RESULTADO_12
    vstr d0, [r0]

    @ IF linha 13
    @ Fonte: ((X) (Y) > IF)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =MEM_Y
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    ble IF_ELSE_13_13

    @ Linha 14
    @ Fonte: (1 SAIDA)
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    ldr r0, =MEM_SAIDA
    vstr d0, [r0]
    ldr r0, =RESULTADO_14
    vstr d0, [r0]
    b IF_FIM_13_14
IF_ELSE_13_13:

    @ Linha 16
    @ Fonte: (0 SAIDA)
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    ldr r0, =MEM_SAIDA
    vstr d0, [r0]
    ldr r0, =RESULTADO_16
    vstr d0, [r0]
IF_FIM_13_14:

    @ WHILE linha 18
    @ Fonte: ((X) 0.0 > WHILE)
WHILE_INICIO_18_15:
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_0_0
    vldr d0, [r0]
    vpop {d1}
    vcmp.f64 d1, d0
    vmrs APSR_nzcv, fpscr
    ble WHILE_FIM_18_16

    @ Linha 19
    @ Fonte: (((X) 1 -) X)
    ldr r0, =MEM_X
    vldr d0, [r0]
    vpush {d0}
    ldr r0, =CONST_1_0
    vldr d0, [r0]
    vpop {d1}
    vsub.f64 d0, d1, d0
    ldr r0, =MEM_X
    vstr d0, [r0]
    ldr r0, =RESULTADO_19
    vstr d0, [r0]
    b WHILE_INICIO_18_15
WHILE_FIM_18_16:

@ ============================================================
@ Impressao dos resultados no JTAG UART
@ ============================================================
    @ Imprime DOBRO
    ldr r1, =STR_DOBRO
    bl print_str
    ldr r0, =MEM_DOBRO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime MEDIA
    ldr r1, =STR_MEDIA
    bl print_str
    ldr r0, =MEM_MEDIA
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime PI
    ldr r1, =STR_PI
    bl print_str
    ldr r0, =MEM_PI
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime POT
    ldr r1, =STR_POT
    bl print_str
    ldr r0, =MEM_POT
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime QUOC
    ldr r1, =STR_QUOC
    bl print_str
    ldr r0, =MEM_QUOC
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime RESTO
    ldr r1, =STR_RESTO
    bl print_str
    ldr r0, =MEM_RESTO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime SAIDA
    ldr r1, =STR_SAIDA
    bl print_str
    ldr r0, =MEM_SAIDA
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime SOMA
    ldr r1, =STR_SOMA
    bl print_str
    ldr r0, =MEM_SOMA
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime ULTIMO
    ldr r1, =STR_ULTIMO
    bl print_str
    ldr r0, =MEM_ULTIMO
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime X
    ldr r1, =STR_X
    bl print_str
    ldr r0, =MEM_X
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str
    @ Imprime Y
    ldr r1, =STR_Y
    bl print_str
    ldr r0, =MEM_Y
    vldr d0, [r0]
    bl print_double
    ldr r1, =STR_NL
    bl print_str

    b fim

@ ============================================================
@ Subrotinas de impressao no JTAG UART (0xFF201000)
@ Polling correto: verifica espaco na FIFO de escrita antes
@ ============================================================

@ print_char: imprime caractere em r2 (espera FIFO ter espaco)
print_char:
    push {r0, r3, lr}
    ldr r0, =0xFF201000
pc_wait:
    ldr r3, [r0, #4]
    lsr r3, r3, #16
    cmp r3, #0
    beq pc_wait
    str r2, [r0]
    pop {r0, r3, lr}
    bx lr

@ print_str: imprime string em r1
print_str:
    push {r2, lr}
ps_loop:
    ldrb r2, [r1], #1
    cmp r2, #0
    beq ps_ret
    bl print_char
    b ps_loop
ps_ret:
    pop {r2, lr}
    bx lr

@ print_int: imprime inteiro em r1
print_int:
    push {r4, r5, r6, r7, lr}
    mov r4, r1
    ldr r6, =PRINT_BUF
    add r6, r6, #11
    mov r7, #0
    strb r7, [r6]
    cmp r4, #0
    bge pi_conv
    ldr r1, =STR_MENOS
    bl print_str
    rsb r4, r4, #0
pi_conv:
    sub r6, r6, #1
    mov r7, r4
    mov r4, #0
pi_d10:
    cmp r7, #10
    blt pi_d10d
    sub r7, r7, #10
    add r4, r4, #1
    b pi_d10
pi_d10d:
    add r7, r7, #48
    strb r7, [r6]
    cmp r4, #0
    bne pi_conv
pi_imp:
    ldrb r2, [r6], #1
    cmp r2, #0
    beq pi_fim
    bl print_char
    b pi_imp
pi_fim:
    pop {r4, r5, r6, r7, lr}
    bx lr

@ print_double: imprime double em d0 com 2 casas decimais
print_double:
    push {r4, r5, lr}
    vmov r4, r5, d0
    tst r5, #0x80000000
    beq pd_pos
    ldr r1, =STR_MENOS
    bl print_str
    vneg.f64 d0, d0
pd_pos:
    vcvt.s32.f64 s0, d0
    vmov r1, s0
    bl print_int
    ldr r1, =STR_PONTO
    bl print_str
    vcvt.f64.s32 d1, s0
    vsub.f64 d0, d0, d1
    ldr r4, =CONST_10_0
    vldr d2, [r4]
    vmul.f64 d0, d0, d2
    vmul.f64 d0, d0, d2
    vcvt.s32.f64 s0, d0
    vmov r1, s0
    cmp r1, #10
    bge pd_2d
    mov r2, #48
    bl print_char
pd_2d:
    bl print_int
    pop {r4, r5, lr}
    bx lr


fim:
    b fim