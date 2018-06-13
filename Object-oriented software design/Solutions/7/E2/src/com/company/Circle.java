package com.company;

import java.awt.*;

class Circle extends AbstractShape {
    private int diameter;
    private Color color;

    Circle(int x, int y, int radius, Color color) {
        this.x = x;
        this.y = y;
        this.diameter = 2 * radius;
        this.color = color;
    }

    @Override
    void drawOn(Graphics g) {
        g.setColor(color);
        int radius = diameter / 2;
        g.drawOval(x - radius, y - radius, diameter, diameter);
    }

    private double distance(double x0, double y0, double x1, double y1) {
        double dx = x0 - x1;
        double dy = y0 - y1;
        return Math.sqrt(dx*dx + dy*dy);
    }

    @Override
    boolean contains(int x, int y) {
        return distance(this.x, this.y, x, y) <= (double) diameter / 2;
    }
}
