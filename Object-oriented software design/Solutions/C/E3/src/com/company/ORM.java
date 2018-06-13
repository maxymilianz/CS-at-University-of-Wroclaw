package com.company;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.List;

public class ORM {
    private Connection connection;

    private Hashtable<Integer, Parent> idToParent;
    private Hashtable<Integer, Child> idToChild;

    public ORM() {
        try {
            connection = DriverManager.getConnection("jdbc:sqlite:db.sqlite");
        }
        catch (Exception e) {
            e.printStackTrace();
        }

        idToParent = new Hashtable<>();
        idToChild = new Hashtable<>();
    }

    public List<Parent> getParents() {
        try {
            ResultSet result = connection.createStatement().executeQuery("select * FROM Parent");
            List<Parent> parents = new LinkedList<>();

            while (result.next()) {
                int id = result.getInt("Id");
                parents.add(new Parent(id));
            }

            return parents;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public List<Child> getChildren() {
        try {
            ResultSet result = connection.createStatement().executeQuery("select * FROM Child");
            List<Child> children = new LinkedList<>();

            while (result.next()) {
                int id = result.getInt("Id");
                int parentId = result.getInt("ParentId");
                children.add(new Child(id, parentFromId(parentId)));
            }

            return children;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public void insertParent(Parent parent) {
        try {
            PreparedStatement statement = connection.prepareStatement("insert INTO Parent VALUES (" + parent.id + ")");
            statement.execute();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void insertChild(Child child) {
        try {
            PreparedStatement statement = connection.prepareStatement("insert INTO Child VALUES (" + child.id + "," + child.parent.id + ")");
            statement.execute();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Parent parentFromId(int id) {
        if (idToParent.containsKey(id))
            return idToParent.get(id);

        try {
            ResultSet result = connection.createStatement().executeQuery("SELECT * FROM Parent");
            Parent parent = null;

            while (result.next()) {
                int someId = result.getInt("Id");

                if (someId == id) {
                    parent = new Parent(someId);
                    break;
                }
            }

            idToParent.put(id, parent);
            return parent;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public Child childFromId(int id) {
        if (idToChild.containsKey(id))
            return idToChild.get(id);

        try {
            ResultSet result = connection.createStatement().executeQuery("SELECT * FROM Child");
            Child child = null;

            while (result.next()) {
                int someId = result.getInt("Id");

                if (someId == id) {
                    child = new Child(someId, parentFromId(result.getInt("ParentInd")));
                    break;
                }
            }

            idToChild.put(id, child);
            return child;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
