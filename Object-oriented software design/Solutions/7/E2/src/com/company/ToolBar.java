package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

class ToolBar extends JToolBar {
    private class Listener implements ActionListener {
        private Hashtable<JButton, Runnable> buttonToRunnable;

        private Listener() {
            buttonToRunnable = new Hashtable<>();
            initButtonToRunnable();
        }

        private void initButtonToRunnable() {
            buttonToRunnable.put(circleButton, () -> changeMode(Mode.CREATE_CIRCLE));
            buttonToRunnable.put(squareButton, () -> changeMode(Mode.CREATE_SQUARE));
            buttonToRunnable.put(rectangleButton, () -> changeMode(Mode.CREATE_RECTANGLE));

            buttonToRunnable.put(moveButton, () -> changeMode(Mode.MOVE));

            buttonToRunnable.put(deleteButton, () -> changeMode(Mode.DELETE));

            buttonToRunnable.put(undoButton, ToolBar.this::undo);
            buttonToRunnable.put(redoButton, ToolBar.this::redo);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            buttonToRunnable.get((JButton) e.getSource()).run();
        }
    }

    private JButton circleButton, squareButton, rectangleButton;
    private JButton moveButton;
    private JButton deleteButton;
    private JButton undoButton, redoButton;

    private JButton highlightedButton;

    private Hashtable<Mode, JButton> modeToButton;

    private Window window;

    ToolBar(Window window) {
        this.window = window;

        circleButton = new JButton("Circle"); squareButton = new JButton("Square"); rectangleButton = new JButton("Rectangle");
        moveButton = new JButton("Move");
        deleteButton = new JButton("Delete");
        undoButton = new JButton("Undo"); redoButton = new JButton("Redo");

        Listener listener = new Listener();

        circleButton.addActionListener(listener); squareButton.addActionListener(listener); rectangleButton.addActionListener(listener);
        moveButton.addActionListener(listener);
        deleteButton.addActionListener(listener);
        undoButton.addActionListener(listener); redoButton.addActionListener(listener);

        add(circleButton); add(squareButton); add(rectangleButton);
        addSeparator();
        add(moveButton);
        addSeparator();
        add(deleteButton);
        addSeparator();
        add(undoButton); add(redoButton);

        modeToButton = new Hashtable<>();
        initModeToButton();
    }

    private void initModeToButton() {
        modeToButton.put(Mode.CREATE_CIRCLE, circleButton); modeToButton.put(Mode.CREATE_SQUARE, squareButton); modeToButton.put(Mode.CREATE_RECTANGLE, rectangleButton);
        modeToButton.put(Mode.DELETE, deleteButton);
        modeToButton.put(Mode.MOVE, moveButton);
    }

    private void highlightButton(JButton button) {
        if (highlightedButton != null)
            highlightedButton.setBackground(null);
        highlightedButton = button;
        button.setBackground(Color.LIGHT_GRAY);
    }

    private void changeMode(Mode mode) {
        window.changeMode(mode);
        highlightButton(modeToButton.get(mode));
    }

    private void undo() {
        window.changeMode(null);
        window.undo();
        if (highlightedButton != null)
            highlightedButton.setBackground(null);
    }

    private void redo() {
        window.changeMode(null);
        window.redo();
        if (highlightedButton != null)
            highlightedButton.setBackground(null);
    }
}
