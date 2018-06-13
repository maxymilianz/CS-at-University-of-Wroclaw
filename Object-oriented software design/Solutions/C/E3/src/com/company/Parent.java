package com.company;

public class Parent {
    private static int lastId = 0;
    public int id;

    public Parent() {
        id = nextId();
    }

    public Parent(int id) {
        this.id = id;
    }

    private static int nextId() {
        return lastId++;
    }

    @Override
    public String toString() {
        return "Parent{" +
                "id=" + id +
                '}';
    }
}
