package com.company;

/**
 * Created by Lenovo on 01.04.2017.
 */
public class Sorter implements Runnable {
    class Elem {
        String val;
        Elem next = null;

        Elem(String value) {
            val = value;
        }

        public int compareTo(String e) {
            return e.compareTo(val);
        }

        public String toString() {
            return val;
        }
    }

    Elem first = null;
    Buffer<String> buffer;

    public Sorter(Buffer<String> buffer) {
        this.buffer = buffer;
    }

    public void add(String value) {
        if (first == null)
            first = new Elem(value);
        else {
            if (first.compareTo(value) < 0) {
                Elem temp = new Elem(value);
                temp.next = first;
                first = temp;
            } else {
                Elem temp = first;

                while (temp.next != null && temp.next.compareTo(value) > 0)
                    temp = temp.next;

                if (temp.next == null)
                    temp.next = new Elem(value);
                else {
                    Elem temp2 = new Elem(value);
                    temp2.next = temp.next;
                    temp.next = temp2;
                }
            }
        }
    }

    public void printAll() {
        Elem temp = first;

        while (temp != null) {
            System.out.println(temp);
            temp = temp.next;
        }
    }

    public void run() {
        while (!buffer.isToClose() || !buffer.empty()) {
            try {
                add(buffer.get());
            }
            catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        printAll();
    }
}
