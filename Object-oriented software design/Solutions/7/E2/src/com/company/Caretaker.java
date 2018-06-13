package com.company;

import java.util.Stack;

class Caretaker {
    private DrawingArea drawingArea;
    private Stack<Memento> undoStack, redoStack;

    Caretaker(DrawingArea drawingArea) {
        this.drawingArea = drawingArea;
        drawingArea.setCaretaker(this);
        undoStack = new Stack<>();
        redoStack = new Stack<>();
    }

    void undo() {
        if (!undoStack.empty()) {
            Memento memento = undoStack.pop();
            drawingArea.undo(memento);
            redoStack.push(memento);
        }
    }

    void redo() {
        if (!redoStack.empty()) {
            Memento memento = redoStack.pop();
            drawingArea.redo(memento);
            undoStack.push(memento);
        }
    }

    void drawingAreaStateChanged(Memento memento) {
        redoStack.clear();
        undoStack.push(memento);
    }
}
