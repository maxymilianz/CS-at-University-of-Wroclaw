package com.company;

/**
 * Created by Lenovo on 24.03.2017.
 */
public class Addition extends Operation {
    public Addition(Expression l, Expression r) {
        left = l;
        right = r;
    }

    /*public double value() {
        return left.value() + right.value();
    }*/

    public String printOp() {
        return " + ";
    }

    protected double operator(double l, double r) {
        return l + r;
    }

    /*public String toString() {
        return "(" + left.toString() + " + " + right.toString() + ")";
    }*/
}
