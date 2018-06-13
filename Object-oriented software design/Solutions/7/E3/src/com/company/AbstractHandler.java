package com.company;

abstract class AbstractHandler {
    AbstractHandler next;

    abstract void handle(String mail);
}
