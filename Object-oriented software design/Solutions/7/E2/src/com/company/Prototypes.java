package com.company;

import java.awt.*;

class Prototypes {
    private static Circle circlePrototype = new Circle(0, 0, 100, Color.GREEN);
    private static Square squarePrototype = new Square(0, 0, 150, Color.ORANGE);
    private static Rectangle rectanglePrototype = new Rectangle(0, 0, 200, 50, Color.RED);

    static Circle getCirclePrototype() {
        return circlePrototype;
    }

    static Square getSquarePrototype() {
        return squarePrototype;
    }

    static Rectangle getRectanglePrototype() {
        return rectanglePrototype;
    }
}
