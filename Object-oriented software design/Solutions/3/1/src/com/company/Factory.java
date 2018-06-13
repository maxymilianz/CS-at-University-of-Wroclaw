package com.company;

/*
Creator - Products should be created through Factory and not directly
 */

public class Factory {
    private int lastId = 0;

    public Factory() {

    }

    public Product makeProduct() {
        return new Product(lastId++);
    }
}
