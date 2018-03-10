package com.company;

/**
 * Created by Lenovo on 25.03.2017.
 */
public abstract class Operation extends Expression {
    Expression left, right;

    protected abstract double operator(double l, double r);

    protected abstract String printOp();

    public double value() {
        return operator(left.value(), right.value());
    }

    public String toString() {
        return "(" + left.toString() + printOp() + right.toString() + ")";
    }
}
