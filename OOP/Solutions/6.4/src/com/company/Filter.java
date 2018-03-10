package com.company;

/**
 * Created by Lenovo on 01.04.2017.
 */
public class Filter implements Runnable {
    String prefix;
    String names[];
    Buffer<String> buffer;

    public Filter(String prefix, String names[], Buffer<String> buffer) {
        this.prefix = prefix;
        this.names = names;
        this.buffer = buffer;
    }

    public boolean prefix(String name) {
        for (int i = 0; i < prefix.length(); i++)
            if (name.charAt(i) != prefix.charAt(i))
                return false;

        return true;
    }

    public void run() {
        for (int i = 0; i < names.length; i++) {
            if (prefix(names[i])) {
                try {
                    buffer.add(names[i]);
                }
                catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        buffer.setToClose(true);
    }
}
