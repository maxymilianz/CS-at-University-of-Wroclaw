package com.company;

class Memento {
    private Operation operation;

    Memento(Operation operation) {
        this.operation = operation;
    }

    Operation getOperation() {
        return operation;
    }
}
