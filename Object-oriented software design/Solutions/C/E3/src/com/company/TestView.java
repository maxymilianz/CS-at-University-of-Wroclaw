package com.company;

import org.jboss.weld.environment.se.Weld;
import org.jboss.weld.environment.se.WeldContainer;

public class TestView {
    private ListController controller;

    public TestView(ListController controller) {
        this.controller = controller;
    }

    private void testParentsList() {
        controller.getParents();
    }

    public void runTests() {
        testParentsList();
    }

    private static void compositionRoot() {
        Weld weld = new Weld();
        WeldContainer container = weld.initialize();
        LocalFactory.setORMProvider(() -> container.select(ORM.class).get());
    }

    public static void main(String[] args) {
        compositionRoot();
        LocalFactory factory = new LocalFactory();
        try {
            new TestView(new ListController(factory.CreateORM()));
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
