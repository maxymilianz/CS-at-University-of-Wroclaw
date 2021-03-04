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

_I_sort_ai_:
    addiu $sp, $sp, -8
    sw $fp, 0($sp)
    sw $ra, 4($sp)
    add $fp, $sp, $zero
    L0:
    ori $at, $zero, 0
    lw $a0, -4($a0)
    L1:
    slt $v0, $at, $a0
    bne $v0, $zero, L2
    L3:
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 8
    jr $ra
    L2:
    addu $v1, $zero, $at
    L4:
    ori $v0, $zero, 0
    slt $v0, $v0, $v1
    bne $v0, $zero, L5
    L6:
    addi $at, $at, 1
    j L1
    L5:
    bne $133, $zero, L7
    L8:
    ori $v0, $zero, 1
    subu $v1, $v1, $v0
    j L4
    L7:
    j L8
_I_main__i:
    addiu $sp, $sp, -12
    sw $fp, 0($sp)
    sw $ra, 4($sp)
    add $fp, $sp, $zero
    L9:
    ori $a0, $zero, 32
    jal _xi_alloc
    sw $v0, 8($fp)
    lw $at, 8($fp)
    addi $at, $at, 4
    sw $at, 8($fp)
    ori $v0, $zero, 7
    lw $at, 8($fp)
    sw $v0, -4($at)
    ori $v0, $zero, 87
    lw $at, 8($fp)
    sw $v0, 0($at)
    ori $v0, $zero, 114
    lw $at, 8($fp)
    sw $v0, 4($at)
    ori $v0, $zero, 111
    lw $at, 8($fp)
    sw $v0, 8($at)
    ori $v0, $zero, 99
    lw $at, 8($fp)
    sw $v0, 12($at)
    ori $v0, $zero, 108
    lw $at, 8($fp)
    sw $v0, 16($at)
    ori $v0, $zero, 97
    lw $at, 8($fp)
    sw $v0, 20($at)
    ori $v0, $zero, 119
    lw $at, 8($fp)
    sw $v0, 24($at)
    lw $a0, 8($fp)
    jal _I_sort_ai_
    lw $a0, 8($fp)
    jal _I_printString_ai_
    ori $v0, $zero, 1
    add $sp, $fp, $zero
    lw $fp, 0($sp)
    lw $ra, 4($sp)
    addiu $sp, $sp, 12
    jr $ra
