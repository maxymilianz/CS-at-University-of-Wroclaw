package com.company;

class CategorySelected implements Notification {
    private User.Category category;

    CategorySelected(User.Category category) {
        this.category = category;
    }

    User.Category getCategory() {
        return category;
    }
}
