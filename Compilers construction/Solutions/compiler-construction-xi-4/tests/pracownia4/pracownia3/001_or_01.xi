printString(str:int[])

pred_lhs():bool
{
    printString("pred_lhs")
    return false
}

pred_rhs():bool
{
    printString("pred_rhs")
    return true
}

main():int
{
    result:int = 3
    if pred_lhs() | pred_rhs() {
        result = 1
    } else {
        result = 0
    }

    return result
}

//@PRACOWNIA
//@out pred_lhs
//@out pred_rhs
//@out Exit code: 1
