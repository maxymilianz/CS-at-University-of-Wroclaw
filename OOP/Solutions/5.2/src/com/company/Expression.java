package com.company;

import java.util.HashMap;

/**
 * Created by Lenovo on 24.03.2017.
 */
public abstract class Expression {
    public static HashMap<String, Double> map;

    public abstract double value();
    public abstract String toString();
}
