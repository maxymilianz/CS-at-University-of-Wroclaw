package com.company;

/*
Low Coupling - I made the Key class instead of explicitly stating that key is an int
 */

public class Car {
    private Key key;
    private boolean opened = false;

    public Car(Key key) {
        this.key = key;
    }

    public void open(Key key) {
        if (key == this.key)
            opened = true;
    }

    public void close(Key key) {
        if (key == this.key)
            opened = false;
    }

    public boolean isOpened() {
        return opened;
    }
}
