package com.company;

import javax.swing.*;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreeSelectionModel;
import java.lang.reflect.Type;
import java.util.*;
import java.util.function.Consumer;

class UsersTree extends JTree implements Subscriber {
    private class SelectionListener implements TreeSelectionListener {
        Hashtable<Type, Consumer<Object>> selectionTypeToResponse;

        SelectionListener() {
            selectionTypeToResponse = new Hashtable<>();
            selectionTypeToResponse.put(User.class, u -> publishUserSelected((User) u));
            selectionTypeToResponse.put(User.Category.class, u -> publishCategorySelected((User.Category) u));
        }

        @Override
        public void valueChanged(TreeSelectionEvent e) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) e.getPath().getLastPathComponent();
            Object object = node.getUserObject();

            Type type = object.getClass();
            if (selectionTypeToResponse.containsKey(type))
                selectionTypeToResponse.get(type).accept(object);
        }
    }

    private EventAggregator eventAggregator;

    private Set<Type> notificationTypes;
    private Hashtable<User.Category, DefaultMutableTreeNode> categoryToNode;
    private DefaultMutableTreeNode root;

    UsersTree(List<User> userList) {
        super(new DefaultMutableTreeNode("Users"));
        getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);
        addTreeSelectionListener(new SelectionListener());
        eventAggregator = EventAggregator.getInstance();
        notificationTypes = new HashSet<>();
        initNotificationTypes();
        categoryToNode = new Hashtable<>();
        initCategoryToNode();
        root = (DefaultMutableTreeNode) getModel().getRoot();

        addUsers(userList);
    }

    private void initNotificationTypes() {
        notificationTypes.add(UserEdited.class);
    }

    private void initCategoryToNode() {
        for (User.Category category : User.Category.values())
            categoryToNode.put(category, new DefaultMutableTreeNode(category));
    }

    private void addUsers(List<User> userList) {
        for (User user : userList)
            categoryToNode.get(user.getCategory()).add(new DefaultMutableTreeNode(user));

        for (DefaultMutableTreeNode node : categoryToNode.values())
            root.add(node);
    }

    private void publishCategorySelected(User.Category category) {
        eventAggregator.publish(new CategorySelected(category));
    }

    private void publishUserSelected(User user) {
        eventAggregator.publish(new UserSelected(user));
    }

    private void handleUserEdited(UserEdited edition) {
        User user = edition.getUser();
        User.Category category = user.getCategory();

        if (!categoryToNode.containsKey(category))
            categoryToNode.put(category, new DefaultMutableTreeNode(category));

        DefaultMutableTreeNode categoryNode = categoryToNode.get(user.getCategory());
        Enumeration<TreeNode> nodes = categoryNode.children();
        boolean userFound = false;

        while (nodes.hasMoreElements()) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) nodes.nextElement();

            if (node.getUserObject() == user)
                userFound = true;
        }

        if (!userFound)
            categoryNode.add(new DefaultMutableTreeNode(user));

        ((DefaultTreeModel) treeModel).reload(categoryNode);
    }

    @Override
    public void handle(Notification notification) {
        assert notification instanceof UserEdited;
        handleUserEdited((UserEdited) notification);
    }

    @Override
    public Set<Type> getNotificationTypes() {
        return notificationTypes;
    }
}
