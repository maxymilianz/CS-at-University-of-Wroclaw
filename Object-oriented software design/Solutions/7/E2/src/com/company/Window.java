package com.company;

import javax.swing.*;
import java.awt.*;

class Window extends JFrame {
    private Caretaker caretaker;
    private DrawingArea drawingArea;

    Window(int width, int height) {
        setTitle("Paint");
        setSize(width, height);
        setLayout(new GridLayout(2, 1));

        add(new ToolBar(this));
        drawingArea = new DrawingArea(this);
        add(drawingArea);

        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);

        caretaker = new Caretaker(drawingArea);
    }

    void changeMode(Mode mode) {
        drawingArea.setMode(mode);
    }

    void undo() {
        caretaker.undo();
    }

    void redo() {
        caretaker.redo();
    }
}
