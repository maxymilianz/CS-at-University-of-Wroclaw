package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class ListView extends JFrame {
    private class Listener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == addParentButton)
                addParent();
            else if (e.getSource() == addChildButton)
                addChild();
        }

        private void addParent() {
            new ParentView(ListView.this);
        }

        private void addChild() {
            new ChildView(ListView.this);
        }
    }

    private DefaultListModel<Parent> parentsListModel;
    private DefaultListModel<Child> childrenListModel;

    private JList<Parent> parentsList;
    private JList<Child> childrenList;

    private JButton addParentButton;
    private JButton addChildButton;

    private ListController controller;

    public ListView(ListController controller) {
        setPreferredSize(new Dimension(400, 300));

        parentsListModel = new DefaultListModel<>();
        childrenListModel = new DefaultListModel<>();

        parentsList = new JList<>(parentsListModel);
        childrenList = new JList<>(childrenListModel);

        setLayout(new GridLayout(2, 2));
        add(parentsList);
        add(childrenList);

        addParentButton = new JButton("Add parent");
        addChildButton = new JButton("Add child");

        Listener listener = new Listener();

        addParentButton.addActionListener(listener);
        addChildButton.addActionListener(listener);

        add(addParentButton);
        add(addChildButton);

        this.controller = controller;

        initParentsList();
        initChildrenList();

        setDefaultCloseOperation(EXIT_ON_CLOSE);
        pack();
        setVisible(true);
    }

    private void initParentsList() {
        for (Parent parent : controller.getParents()) {
            parentsListModel.addElement(parent);
        }
    }

    private void initChildrenList() {
        for (Child child : controller.getChildren()) {
            childrenListModel.addElement(child);
        }
    }

    public void addParent(Parent parent) {
        controller.addParent(parent);
        parentsListModel.addElement(parent);
    }

    public void addChild(Child child) {
        controller.addChild(child);
        childrenListModel.addElement(child);
    }
}
