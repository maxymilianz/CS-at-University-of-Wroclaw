package com.company;

import javax.swing.*;
import java.awt.*;
import java.util.List;

class Window extends JFrame {
    private EventAggregator eventAggregator;

    private UsersTree users;
    private WorkingPanel workingPanel;

    Window(List<User> userList) {
        setLayout(new GridLayout(1, 2));
        setTitle("User registry");
        setPreferredSize(new Dimension(200, 300));

        Container container = getContentPane();

        users = new UsersTree(userList);
        container.add(users);

        workingPanel = new WorkingPanel(userList, this);
        container.add(workingPanel);

        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setVisible(true);

        eventAggregator = EventAggregator.getInstance();
        addSubscribers();
    }

    private void addSubscribers() {
        eventAggregator.addSubscriber(users);
        eventAggregator.addSubscriber(workingPanel);
    }
}
