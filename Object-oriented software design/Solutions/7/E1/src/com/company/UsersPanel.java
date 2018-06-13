package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

class UsersPanel extends JPanel {
    private class Listener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            new EditUserDialog(currentCategory, window);
        }
    }

    private Hashtable<User.Category, JList<User>> categoryToUsers;
    private User.Category currentCategory;
    private Window window;

    UsersPanel(Hashtable<User.Category, List<User>> categoryToUserList, Window window) {
        this.window = window;

        categoryToUsers = new Hashtable<>();
        initCategoryToUsers(categoryToUserList);

        setLayout(new GridLayout(2, 1));

        JButton addButton = new JButton("Add user");
        addButton.addActionListener(new Listener());
        addAndRepaint(addButton);
    }

    private void initCategoryToUsers(Hashtable<User.Category, List<User>> categoryToUserList) {
        for (Map.Entry<User.Category, List<User>> entry : categoryToUserList.entrySet()) {
            User.Category category = entry.getKey();

            if (!categoryToUsers.containsKey(category)) {
                JList<User> userJList = new JList<>();
                userJList.setModel(new DefaultListModel<>());
                userJList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
                userJList.setLayoutOrientation(JList.HORIZONTAL_WRAP);
                categoryToUsers.put(category, userJList);
            }

            DefaultListModel<User> listModel = (DefaultListModel<User>) categoryToUsers.get(category).getModel();

            for (User user : entry.getValue())
                listModel.addElement(user);
        }
    }

    void displayUsers(User.Category category) {
        if (currentCategory != null)
            remove(categoryToUsers.get(currentCategory));
        currentCategory = category;
        addAndRepaint(categoryToUsers.get(category), 0);
    }

    void updateUserJList(User user) {
        DefaultListModel<User> listModel = (DefaultListModel<User>) categoryToUsers.get(user.getCategory()).getModel();

        if (!listModel.contains(user))
            listModel.addElement(user);
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
