package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class UserDetailsPanel extends JPanel {
    private class Listener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            new EditUserDialog(currentUser, window);
        }
    }

    private JTextArea nameArea;
    private Window window;

    private User currentUser;

    UserDetailsPanel(Window window) {
        setLayout(new GridLayout(3, 1));

        JTextArea name = new JTextArea("Name:");
        name.setEditable(false);
        addAndRepaint(name);

        nameArea = new JTextArea();
        nameArea.setEditable(false);
        addAndRepaint(nameArea);

        JButton editButton = new JButton("Edit user");
        editButton.addActionListener(new Listener());
        addAndRepaint(editButton);

        this.window = window;
    }

    void displayUser(User user) {
        currentUser = user;
        nameArea.setText(user.toString());
    }

    private void addAndRepaint(Component component) {
        addAndRepaint(component, getComponentCount());
    }

    private void addAndRepaint(Component component, int position) {
        add(component, position);
        revalidate();
        repaint();
    }
}
