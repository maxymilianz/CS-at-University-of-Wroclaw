package com.company;

/**
 * Created by Lenovo on 24.03.2017.
 */
public class Variable extends Expression {
    String val;

    public Variable(String arg) {
        val = arg;
    }

    public double value() {
        return Expression.map.get(val);
    }

    public String toString() {
        return val;
    }
}
