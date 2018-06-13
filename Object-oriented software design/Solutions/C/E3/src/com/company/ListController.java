package com.company;

import java.util.List;

public class ListController {
    private ORM orm;

    public ListController(ORM orm) {
        this.orm = orm;
    }

    public void addParent(Parent parent) {
        orm.insertParent(parent);
    }

    public void addChild(Child child) {
        orm.insertChild(child);
    }

    public List<Parent> getParents() {
        return orm.getParents();
    }

    public List<Child> getChildren() {
        return orm.getChildren();
    }
}
