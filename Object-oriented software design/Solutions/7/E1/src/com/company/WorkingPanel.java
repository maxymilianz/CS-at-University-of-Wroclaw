package com.company;

import javax.swing.*;
import java.awt.*;
import java.lang.reflect.Type;
import java.util.*;
import java.util.List;
import java.util.function.Consumer;

class WorkingPanel extends JPanel implements Subscriber {
    private Set<Type> notificationTypes;
    private Hashtable<Type, Consumer<Notification>> notificationHandlers;

    private Hashtable<User.Category, List<User>> categoryToUsers;

    private UsersPanel users;
    private UserDetailsPanel userDetails;

    WorkingPanel(List<User> userList, Window window) {
        categoryToUsers = new Hashtable<>();
        initCategoryToUsers(userList);

        notificationTypes = new HashSet<>();
        initNotificationTypes();

        notificationHandlers = new Hashtable<>();
        initNotificationHandlers();

        users = new UsersPanel(categoryToUsers, window);
        userDetails = new UserDetailsPanel(window);
    }

    private void initCategoryToUsers(List<User> userList) {
        for (User user : userList) {
            User.Category category = user.getCategory();

            if (!categoryToUsers.containsKey(category))
                categoryToUsers.put(category, new LinkedList<>());

            categoryToUsers.get(category).add(user);
        }
    }

    private void initNotificationTypes() {
        notificationTypes.add(CategorySelected.class);
        notificationTypes.add(UserSelected.class);
        notificationTypes.add(UserEdited.class);
    }

    private void initNotificationHandlers() {
        notificationHandlers.put(CategorySelected.class, s -> handleCategorySelected((CategorySelected) s));
        notificationHandlers.put(UserSelected.class, s -> handleUserSelected((UserSelected) s));
        notificationHandlers.put(UserEdited.class, e -> handleUserEdited((UserEdited) e));
    }

    private void handleCategorySelected(CategorySelected selection) {
        users.displayUsers(selection.getCategory());
        removeAll();
        addAndRepaint(users);
    }

    private void handleUserSelected(UserSelected selection) {
        userDetails.displayUser(selection.getUser());
        removeAll();
        addAndRepaint(userDetails);
    }

    private void handleUserEdited(UserEdited edition) {
        users.updateUserJList(edition.getUser());
    }

    @Override
    public void handle(Notification notification) {
        notificationHandlers.get(notification.getClass()).accept(notification);
    }

    @Override
    public Set<Type> getNotificationTypes() {
        return notificationTypes;
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
