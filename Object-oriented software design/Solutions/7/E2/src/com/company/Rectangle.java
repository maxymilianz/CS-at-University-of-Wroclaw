package com.company;

import java.awt.*;

class Rectangle extends AbstractShape {
    private int w, h;
    private Color color;

    Rectangle(int x, int y, int w, int h, Color color) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.color = color;
    }

    @Override
    void drawOn(Graphics g) {
        g.setColor(color);
        g.drawRect(x, y, w, h);
    }

    private boolean between(int a, int b, int m) {
        return (a <= m && m <= b) || (a >= m && m >= b);
    }

    @Override
    boolean contains(int x, int y) {
        return between(this.x, this.x + w, x) && between(this.y, this.y + h, y);
    }
}
