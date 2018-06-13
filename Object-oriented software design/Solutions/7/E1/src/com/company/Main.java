package com.company;

import java.util.LinkedList;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        List<User> users = new LinkedList<>();
        users.add(new User("AS", User.Category.ADMIN));
        users.add(new User("MZ", User.Category.ADMIN));
        users.add(new User("MD", User.Category.ADMIN));
        users.add(new User("WG", User.Category.USER));
        users.add(new User("KD", User.Category.USER));
        users.add(new User("SP", User.Category.USER));
        users.add(new User("bs", User.Category.GUEST));
        users.add(new User("ms", User.Category.GUEST));
        users.add(new User("am", User.Category.GUEST));

        Window w = new Window(users);
    }
}
