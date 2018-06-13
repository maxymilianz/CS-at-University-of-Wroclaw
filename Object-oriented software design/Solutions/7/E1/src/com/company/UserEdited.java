package com.company;

class UserEdited implements Notification {
    private User user;

    UserEdited(User user) {
        this.user = user;
    }

    User getUser() {
        return user;
    }
}
