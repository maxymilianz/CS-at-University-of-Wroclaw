package com.company;

/**
 * Created by Lenovo on 06.04.2017.
 */
public class Car extends Vehicle {
    public int power;
    public int torque;

    public Car() {
        super();
        power = 0;
        torque = 0;
    }

    /*public Car(String manufacturer, String model, int maxSpeed, double acc0To100, int power, int torque) {
        this.manufacturer = manufacturer;
        this.model = model;
        this.maxSpeed = maxSpeed;
        this.acc0To100 = acc0To100;
        this.power = power;
        this.torque = torque;
    }*/

    public String toString() {
        return super.toString() + ", power: " + power + ", torque: " + torque;
    }
}
