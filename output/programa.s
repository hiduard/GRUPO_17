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

fim:
    b fim