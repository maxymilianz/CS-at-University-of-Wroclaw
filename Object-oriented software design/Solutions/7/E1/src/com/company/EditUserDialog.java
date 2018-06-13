package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

class EditUserDialog extends JDialog {
    private class Listener implements ActionListener {      // this could be done better, like in UsersTree
        private Hashtable<JButton, Runnable> buttonToRunnable;

        Listener() {
            buttonToRunnable = new Hashtable<>();
            buttonToRunnable.put(saveButton, EditUserDialog.this::publishUserAdded);
            buttonToRunnable.put(cancelButton, EditUserDialog.this::dispose);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            buttonToRunnable.get(((JButton) e.getSource())).run();
        }
    }

    private EventAggregator eventAggregator;

    private User user;

    private JTextArea nameArea;
    private JButton saveButton, cancelButton;

    EditUserDialog(User.Category category, JFrame owner) {
        this(new User("", category), owner);
    }

    EditUserDialog(User user, JFrame owner) {
        super(owner, ModalityType.DOCUMENT_MODAL);
        setTitle("Editing user");
        setLayout(new GridLayout(2, 2));

        JTextArea name = new JTextArea("Name:");
        name.setEditable(false);
        addAndRepaint(name);

        nameArea = new JTextArea(user.getName());
        addAndRepaint(nameArea);
        
        saveButton = new JButton("Save");
        addAndRepaint(saveButton);

        cancelButton = new JButton("Cancel");
        addAndRepaint(cancelButton);

        Listener listener = new Listener();
        saveButton.addActionListener(listener);
        cancelButton.addActionListener(listener);

        eventAggregator = EventAggregator.getInstance();
        this.user = user;

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        pack();
        setVisible(true);
    }

    private void publishUserAdded() {
        user.setName(nameArea.getText());
        eventAggregator.publish(new UserEdited(user));
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
