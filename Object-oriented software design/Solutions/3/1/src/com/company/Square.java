package com.company;

import javafx.geometry.Point2D;

public class Square extends Figure {
    private Point2D ul, ur, lr, ll;     // upper left, right and lower

    public Square(Point2D ul, Point2D ur, Point2D lr, Point2D ll) {
        this.ul = ul;
        this.ur = ur;
        this.lr = lr;
        this.ll = ll;
    }

    @Override
    public void print() {
        System.out.println(ul + " " + ur + " " + lr + " " + ll);
    }
}
