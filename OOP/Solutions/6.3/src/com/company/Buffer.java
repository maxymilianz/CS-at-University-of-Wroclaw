package com.company;

/**
 * Created by Lenovo on 01.04.2017.
 */
public class Buffer<T> {
    class Elem<T> {
        T val;
        Elem prev;

        Elem(T value) {
            val = value;
            prev = null;
        }

        T getVal() {
            return val;
        }

        Elem getPrev() {
            return prev;
        }

        void setPrev(Elem prev) {
            this.prev = prev;
        }

        /*private Elem getNext() {
            return next;
        }

        private void setNext(Elem next) {
            this.next = next;
        }*/
    }

    int size, maxSize;
    Elem<T> first, last;

    public Buffer(int val) {
        size = 0;
        maxSize = val;
        first = null;
        last = null;
    }

    public synchronized void add(T val) throws InterruptedException {
        if (full())
            wait();

        if (first == null) {
            first = new Elem<T>(val);
            last = first;
        }
        else {
            Elem temp = new Elem<T>(val);
            //temp.setNext(first);
            //temp.getNext().setPrev(temp);
            first.setPrev(temp);
            first = temp;
        }

        size++;
        notify();
    }

    public synchronized T get() throws InterruptedException {
        if (empty())
            wait();

        size--;
        T temp = last.getVal();
        //last.getPrev().setNext(null);
        if (first == last)
            first = null;
        last = last.getPrev();
        notify();

        return temp;
    }

    public boolean full() {
        return size == maxSize;
    }

    public boolean empty() {
        return size == 0;
    }
}
