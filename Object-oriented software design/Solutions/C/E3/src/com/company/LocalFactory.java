package com.company;

import java.util.concurrent.Callable;

public class LocalFactory {
    private static Callable<ORM> ORMProvider;

    public ORM CreateORM() throws Exception {
        if (ORMProvider == null)
            throw new Exception("No ORM provider");

        return ORMProvider.call();
    }

    public static Callable<ORM> getORMProvider() {
        return ORMProvider;
    }

    public static void setORMProvider(Callable<ORM> ORMProvider) {
        LocalFactory.ORMProvider = ORMProvider;
    }
}
