package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

public class ChildView extends JDialog {
    private class Listener implements ActionListener {      // this could be done better, like in UsersTree
        private Hashtable<JButton, Runnable> buttonToRunnable;

        Listener() {
            buttonToRunnable = new Hashtable<>();
            buttonToRunnable.put(saveButton, ChildView.this::publishChildAdded);
            buttonToRunnable.put(cancelButton, ChildView.this::dispose);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            buttonToRunnable.get(((JButton) e.getSource())).run();
        }
    }

    private Child child;

    private ListView owner;

    private JTextArea idArea, parentIdArea;
    private JButton saveButton, cancelButton;

    public ChildView(ListView owner) {
        this(new Child(0, null), owner);
    }

    public ChildView(Child child, ListView owner) {
        super(owner, Dialog.ModalityType.DOCUMENT_MODAL);
        setTitle("Editing child");
        setLayout(new GridLayout(3, 2));

        JTextArea id = new JTextArea("Id:");
        id.setEditable(false);
        addAndRepaint(id);

        idArea = new JTextArea(Integer.toString(child.id));
        addAndRepaint(idArea);

        JTextArea parentsId = new JTextArea("Parents id:");
        parentsId.setEditable(false);
        addAndRepaint(parentsId);

        parentIdArea = new JTextArea(Integer.toString(0));
        addAndRepaint(parentIdArea);

        saveButton = new JButton("Save");
        addAndRepaint(saveButton);

        cancelButton = new JButton("Cancel");
        addAndRepaint(cancelButton);

        ChildView.Listener listener = new ChildView.Listener();
        saveButton.addActionListener(listener);
        cancelButton.addActionListener(listener);

        this.owner = owner;
        this.child = child;

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        pack();
        setVisible(true);
    }

    private void publishChildAdded() {
        child.id = Integer.parseInt(idArea.getText());
        child.parent = new Parent(Integer.parseInt(parentIdArea.getText()));
        owner.addChild(child);
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
