.data
endline: .asciiz "\n"
endmessage: .asciiz "Exit code: "

.text
.set noat

main:
   add $sp, $sp, -4
   sw $ra, 4($sp)
   jal _I_main__i
   move $a1, $v0
   la $a0, endmessage
   li $v0, 4
   syscall
   li $v0, 1
   move $a0, $a1
   syscall
   la $a0, endline
   li $v0, 4
   syscall
   lw $ra, 4($sp)
   add $sp, $sp, 4
   jr $ra

_xi_length:
   lw $v0, -4($a0)
   jr $ra

_xi_concat:
   # t0 = lhs
   # t1 = rhs
   move $t0, $a0
   move $t1, $a1
   # t2 = len(lhs)
   # t3 = len(rhs)
   lw $t2, -4($t0)
   lw $t3, -4($t1)
   # t4 = len(lhs) + len(rhs)
   addu $t4, $t2, $t3
   # v0 = malloc(4*t4+4) 
   li $t5, 4
   mul $a0, $t4, $t5
   addiu $a0, $a0, 4
   li $v0, 9
   syscall
   addiu $v0, $v0, 4
   sw $t4, -4($v0)
   move $v1, $v0
   XL0:
   beq $zero, $t2, XL1
   lw $t4, 0($t0)
   sw $t4, 0($v1)
   addiu $t2, $t2, -1
   addiu $t0, $t0, 4
   addiu $v1, $v1, 4
   j XL0
   XL1:
   beq $zero, $t3, XL2
   lw $t4, 0($t1)
   sw $t4, 0($v1)
   addiu $t3, $t3, -1
   addiu $t1, $t1, 4
   addiu $v1, $v1, 4
   j XL1
   XL2:
   jr $ra

_xi_alloc:
   li $v0, 9
   syscall
   jr $ra

_I_printString_ai_:
   # t0 = len a0
   move $t1, $a0
   lw $t0, -4($t1)
   mul $a0, $t0, 4
   addiu $a0, $a0, 2
   li $v0, 9
   syscall
   move $a0, $v0
   move $v1, $v0
   XL10:
   beq $zero, $t0, XL11
   lw $t2, 0($t1)
   sb $t2, 0($v1)
   addiu $t0, $t0, -1
   addu $t1, $t1, 4
   addu $v1, $v1, 1
   j XL10
   XL11:
   li $t0, 10
   sb $t0, 0($v1)
   sb $zero, 1($v1)
   li $v0, 4
   syscall
   jr $ra


_I_printInt_i_:
   li $v0, 1
   syscall
   li $v0, 4
   la $a0, endline
   syscall
   jr $ra

_I_pred_lhs__b:
    addiu $sp, $sp, -8
    sw $fp, 0($sp)
    sw $ra, 4($sp)
    add $fp, $sp, $zero
    L0:
    ori $a0, $zero, 36
    jal _xi_alloc
    addu $a0, $zero, $v0
    addi $a0, $a0, 4
    ori $at, $zero, 8
    sw $at, -4($a0)
    ori $at, $zero, 112
    sw $at, 0($a0)
    ori $at, $zero, 114
    sw $at, 4($a0)
    ori $at, $zero, 101
    sw $at, 8($a0)
    ori $at, $zero, 100
    sw $at, 12($a0)
    ori $at, $zero, 95
    sw $at, 16($a0)
    ori $at, $zero, 108
    sw $at, 20($a0)
    ori $at, $zero, 104
    sw $at, 24($a0)
    ori $at, $zero, 115
    sw $at, 28($a0)
    jal _I_printString_ai_
    ori $v0, $zero, 0
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 8
    jr $ra
_I_pred_rhs__b:
    addiu $sp, $sp, -8
    sw $fp, 0($sp)
    sw $ra, 4($sp)
    add $fp, $sp, $zero
    L1:
    ori $a0, $zero, 36
    jal _xi_alloc
    addu $a0, $zero, $v0
    addi $a0, $a0, 4
    ori $at, $zero, 8
    sw $at, -4($a0)
    ori $at, $zero, 112
    sw $at, 0($a0)
    ori $at, $zero, 114
    sw $at, 4($a0)
    ori $at, $zero, 101
    sw $at, 8($a0)
    ori $at, $zero, 100
    sw $at, 12($a0)
    ori $at, $zero, 95
    sw $at, 16($a0)
    ori $at, $zero, 114
    sw $at, 20($a0)
    ori $at, $zero, 104
    sw $at, 24($a0)
    ori $at, $zero, 115
    sw $at, 28($a0)
    jal _I_printString_ai_
    ori $v0, $zero, 1
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 8
    jr $ra
_I_main__i:
    addiu $sp, $sp, -8
    sw $fp, 0($sp)
    sw $ra, 4($sp)
    add $fp, $sp, $zero
    L2:
    jal _I_pred_lhs__b
    ori $at, $zero, 0
    bne $v0, $at, L3
    L4:
    jal _I_pred_rhs__b
    ori $at, $zero, 0
    bne $v0, $at, L3
    L5:
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 8
    jr $ra
    L3:
    ori $v0, $zero, 3
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 8
    jr $ra
