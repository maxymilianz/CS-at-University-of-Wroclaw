package com.company;

/*
Information Expert - worker knows at which machine he works, so he turns it on and off. Alternatively, these methods
could be done by factory, but then it would have to be checked what machine a worker works at.
 */

public class Worker {
    private int machine;        // machine the worker works at in factory
    private boolean machineOn = false;

    public Worker(int machine) {
        this.machine = machine;
    }

    public void turnOffMachine() {
        machineOn = false;
    }

    public void turnOnMachine() {
        machineOn = true;
    }

    public boolean isMachineOn() {
        return machineOn;
    }
}
