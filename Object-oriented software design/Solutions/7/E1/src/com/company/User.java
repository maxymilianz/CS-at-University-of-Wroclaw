package com.company;

class User {
    enum Category {
        ADMIN,
        USER,
        GUEST
    }

    private String name;

    private Category category;

    User(String name, Category category) {
        this.name = name;
        this.category = category;
    }

    String getName() {
        return name;
    }

    void setName(String name) {
        this.name = name;
    }

    Category getCategory() {
        return category;
    }

    @Override
    public String toString() {
        return name;
    }
}
