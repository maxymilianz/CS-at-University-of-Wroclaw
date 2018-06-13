package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

public class ParentView extends JDialog {
    private class Listener implements ActionListener {      // this could be done better, like in UsersTree
        private Hashtable<JButton, Runnable> buttonToRunnable;

        Listener() {
            buttonToRunnable = new Hashtable<>();
            buttonToRunnable.put(saveButton, ParentView.this::publishParentAdded);
            buttonToRunnable.put(cancelButton, ParentView.this::dispose);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            buttonToRunnable.get(((JButton) e.getSource())).run();
        }
    }

    private Parent parent;

    private ListView owner;

    private JTextArea idArea;
    private JButton saveButton, cancelButton;

    public ParentView(ListView owner) {
        this(new Parent(0), owner);
    }

    public ParentView(Parent parent, ListView owner) {
        super(owner, ModalityType.DOCUMENT_MODAL);
        setTitle("Editing parent");
        setLayout(new GridLayout(2, 2));

        JTextArea id = new JTextArea("Id:");
        id.setEditable(false);
        addAndRepaint(id);

        idArea = new JTextArea(Integer.toString(parent.id));
        addAndRepaint(idArea);

        saveButton = new JButton("Save");
        addAndRepaint(saveButton);

        cancelButton = new JButton("Cancel");
        addAndRepaint(cancelButton);

        Listener listener = new Listener();
        saveButton.addActionListener(listener);
        cancelButton.addActionListener(listener);

        this.owner = owner;
        this.parent = parent;

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        pack();
        setVisible(true);
    }

    private void publishParentAdded() {
        parent.id = Integer.parseInt(idArea.getText());
        owner.addParent(parent);
    }

    private void addAndRepaint(Component component) {
        add(component);
        revalidate();
        repaint();
    }

    private void addAndRepaint(Component component, int position) {
        add(component, position);
        revalidate();
        repaint();
    }
}
