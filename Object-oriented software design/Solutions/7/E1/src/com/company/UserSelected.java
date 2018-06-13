package com.company;

class UserSelected implements Notification {
    private User user;

    UserSelected(User user) {
        this.user = user;
    }

    User getUser() {
        return user;
    }
}
