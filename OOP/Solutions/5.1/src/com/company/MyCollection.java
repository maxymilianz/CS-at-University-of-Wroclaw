package com.company;

import javafx.application.Application;

/**
 * Created by Lenovo on 25.03.2017.
 */
public class MyCollection<T> {
    class Elem<T> implements Comparable<T> {
        T val;
        Elem<T> next = null;

        Elem(T value) {
            val = value;
        }

        public int compareTo(T e) {
            return ((Comparable) e).compareTo(val);
        }

        public String toString() {
            return val.toString();
        }
    }

    Elem<T> first;

    public MyCollection() {
        first = null;
    }

    public void add(T value) {
        if (first == null)
            first = new Elem<>(value);
        else {
            if (first.compareTo(value) < 0) {
                Elem<T> temp = new Elem<>(value);
                temp.next = first;
                first = temp;
            } else {
                Elem<T> temp = first;

                while (temp.next != null && temp.next.compareTo(value) > 0)
                    temp = temp.next;

                if (temp.next == null)
                    temp.next = new Elem<>(value);
                else {
                    Elem<T> temp2 = new Elem<>(value);
                    temp2.next = temp.next;
                    temp.next = temp2;
                }
            }
        }
    }

    public Elem<T> get() {
        Elem<T> temp = first;
        if (first != null)
            first = first.next;
        return temp;
    }

    public void printAll() {
        Elem<T> temp = first;

        while (temp != null) {
            System.out.println(temp);
            temp = temp.next;
        }
    }
}
