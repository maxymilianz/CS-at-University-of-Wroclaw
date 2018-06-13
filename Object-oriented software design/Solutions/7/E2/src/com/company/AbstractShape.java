package com.company;

import java.awt.*;

abstract class AbstractShape implements Cloneable {
    int x, y;

    abstract void drawOn(Graphics g);

    abstract boolean contains(int x, int y);

    void move(int dx, int dy) {
        x -= dx;
        y -= dy;
    }

    void setX(int x) {
        this.x = x;
    }

    void setY(int y) {
        this.y = y;
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
