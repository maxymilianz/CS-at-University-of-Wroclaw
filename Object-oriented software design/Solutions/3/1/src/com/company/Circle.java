package com.company;

import javafx.geometry.Point2D;

public class Circle extends Figure {
    private Point2D center;
    private float radius;

    public Circle(Point2D center, float radius) {
        this.center = center;
        this.radius = radius;
    }

    @Override
    public void print() {
        System.out.println("Center = " + center + ", radius = " + radius);
    }
}
