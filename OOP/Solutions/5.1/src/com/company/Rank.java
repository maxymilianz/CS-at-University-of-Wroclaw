package com.company;

/**
 * Created by Lenovo on 25.03.2017.
 */
public abstract class Rank implements Comparable<Rank> {
    Float val;
    String name;

    public String toString() {
        return name + ", " + val;
    }

    public Float getVal() {
        return val;
    }

    public int compareTo(Rank r) {
        return val.compareTo(r.val);
    }
}
