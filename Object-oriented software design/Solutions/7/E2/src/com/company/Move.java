package com.company;

class Move extends Operation {
    private int newX, newY, oldX, oldY;

    Move(AbstractShape shape, int newX, int newY, int oldX, int oldY) {
        this.shape = shape;
        this.newX = newX;
        this.newY = newY;
        this.oldX = oldX;
        this.oldY = oldY;
    }

    public int getNewX() {
        return newX;
    }

    public int getNewY() {
        return newY;
    }

    public int getOldX() {
        return oldX;
    }

    public int getOldY() {
        return oldY;
    }
}
