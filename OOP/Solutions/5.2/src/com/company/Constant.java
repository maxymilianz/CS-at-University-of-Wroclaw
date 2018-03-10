package com.company;

/**
 * Created by Lenovo on 24.03.2017.
 */
public class Constant extends Expression {
    double val;

    public Constant(double arg) {
        val = arg;
    }

    public double value() {
        return val;
    }

    public String toString() {
        return Double.toString(val);
    }
}
