package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.lang.reflect.Type;
import java.util.*;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Consumer;

class DrawingArea extends JPanel {
    private class Listener implements MouseListener {
        private int pressX, pressY;

        private Hashtable<Mode, BiConsumer<Integer, Integer>> modeToConsumer;

        private Listener() {
            modeToConsumer = new Hashtable<>();
            initModeToConsumer();

            modeToPrototype = new Hashtable<>();
            initModeToPrototype();
        }

        private void initModeToConsumer() {
            modeToConsumer.put(Mode.CREATE_CIRCLE, DrawingArea.this::addShape);
            modeToConsumer.put(Mode.CREATE_SQUARE, DrawingArea.this::addShape);
            modeToConsumer.put(Mode.CREATE_RECTANGLE, DrawingArea.this::addShape);

            modeToConsumer.put(Mode.DELETE, DrawingArea.this::deleteShape);
        }

        @Override
        public void mouseClicked(MouseEvent e) {
            if (mode != null)
                modeToConsumer.get(mode).accept(e.getX(), e.getY());
        }

        @Override
        public void mousePressed(MouseEvent e) {
            pressX = e.getX();
            pressY = e.getY();
        }

        @Override
        public void mouseReleased(MouseEvent e) {
            if (mode == Mode.MOVE)
                moveShape(pressX - e.getX(), pressY - e.getY(), shapeAt(pressX, pressY));
        }

        @Override
        public void mouseEntered(MouseEvent e) {

        }

        @Override
        public void mouseExited(MouseEvent e) {

        }
    }

    private Window window;

    private Hashtable<Mode, AbstractShape> modeToPrototype;

    private Hashtable<Type, Consumer<Operation>> operationTypeToUndo;
    private Hashtable<Type, Consumer<Operation>> operationTypeToRedo;

    private List<AbstractShape> shapes;

    private Caretaker caretaker;

    private Mode mode;

    DrawingArea(Window window) {
        this.window = window;
        shapes = new LinkedList<>();
        addMouseListener(new Listener());

        modeToPrototype = new Hashtable<>();
        initModeToPrototype();

        operationTypeToUndo = new Hashtable<>();
        initOperationTypeToUndo();

        operationTypeToRedo = new Hashtable<>();
        initOperationTypeToRedo();
    }

    private void initModeToPrototype() {
        modeToPrototype.put(Mode.CREATE_CIRCLE, Prototypes.getCirclePrototype());
        modeToPrototype.put(Mode.CREATE_SQUARE, Prototypes.getSquarePrototype());
        modeToPrototype.put(Mode.CREATE_RECTANGLE, Prototypes.getRectanglePrototype());
    }

    private void initOperationTypeToUndo() {
        operationTypeToUndo.put(Creation.class, this::undoCreation);
        operationTypeToUndo.put(Move.class, this::undoMove);
        operationTypeToUndo.put(Deletion.class, this::undoDeletion);
    }

    private void initOperationTypeToRedo() {
        operationTypeToRedo.put(Creation.class, this::redoCreation);
        operationTypeToRedo.put(Move.class, this::redoMove);
        operationTypeToRedo.put(Deletion.class, this::redoDeletion);
    }

    void undo(Memento memento) {
        Operation operation = memento.getOperation();
        operationTypeToUndo.get(operation.getClass()).accept(operation);
        window.repaint();
    }

    void redo(Memento memento) {
        Operation operation = memento.getOperation();
        operationTypeToRedo.get(operation.getClass()).accept(operation);
        window.repaint();
    }

    private void undoCreation(Operation operation) {
        shapes.remove(operation.getShape());
    }

    private void undoMove(Operation operation) {
        Move move = (Move) operation;
        move.getShape().move(move.getNewX() - move.getOldX(), move.getNewY() - move.getOldY());
    }

    private void undoDeletion(Operation operation) {
        shapes.add(operation.getShape());
    }

    private void redoCreation(Operation operation) {
        shapes.add(operation.getShape());
    }

    private void redoMove(Operation operation) {
        Move move = (Move) operation;
        move.getShape().move(-move.getNewX() + move.getOldX(), -move.getNewY() + move.getOldY());
    }

    private void redoDeletion(Operation operation) {
        shapes.remove(operation.getShape());
    }

    private AbstractShape shapeAt(int x, int y) {
        for (AbstractShape shape : shapes)
            if (shape.contains(x, y))
                return shape;

        return null;
    }

    private void addShape(int x, int y) {
        if (!modeToPrototype.containsKey(mode))
            return;

        try {
            AbstractShape shape = (AbstractShape) modeToPrototype.get(mode).clone();
            shape.setX(x);
            shape.setY(y);
            shapes.add(shape);
            window.repaint();

            caretaker.drawingAreaStateChanged(new Memento(new Creation(shape)));
        }
        catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
    }

    private void moveShape(int dx, int dy, AbstractShape shape) {
        if (shape != null) {
            caretaker.drawingAreaStateChanged(new Memento(new Move(shape, shape.x, shape.y, shape.x + dx, shape.y + dy)));
            shape.move(dx, dy);
            window.repaint();
        }
    }

    private void deleteShape(int x, int y) {
        AbstractShape shape = shapeAt(x, y);

        if (shape != null) {
            caretaker.drawingAreaStateChanged(new Memento(new Deletion(shape)));
            shapes.remove(shape);
            window.repaint();
        }
    }

    @Override
    public void paint(Graphics g) {
        for (AbstractShape shape : shapes)
            shape.drawOn(g);
    }

    void setMode(Mode mode) {
        this.mode = mode;
    }

    void setCaretaker(Caretaker caretaker) {
        this.caretaker = caretaker;
    }
}
