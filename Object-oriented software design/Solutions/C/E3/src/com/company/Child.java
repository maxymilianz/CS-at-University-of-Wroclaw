package com.company;

public class Child {
    private static int lastId = 0;
    public int id;
    public Parent parent;

    public Child(Parent parent) {
        id = nextId();
        this.parent = parent;
    }

    public Child(int id, Parent parent) {
        this.id = id;
        this.parent = parent;
    }

    private static int nextId() {
        return lastId++;
    }

    @Override
    public String toString() {
        return "Child{" +
                "id=" + id +
                ", parent=" + parent +
                '}';
    }
}
