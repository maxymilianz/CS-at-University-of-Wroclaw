package com.company;

import java.awt.*;

class Square extends AbstractShape {
    private int size;
    private Color color;

    Square(int x, int y, int size, Color color) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = color;
    }

    @Override
    void drawOn(Graphics g) {
        g.setColor(color);
        g.drawRect(x, y, size, size);
    }

    private boolean between(int a, int b, int m) {
        return (a <= m && m <= b) || (a >= m && m >= b);
    }

    @Override
    boolean contains(int x, int y) {
        return between(this.x, this.x + size, x) && between(this.y, this.y + size, y);
    }
}
