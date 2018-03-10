package com.company;

/**
 * Created by Lenovo on 06.04.2017.
 */
public class Car extends Vehicle {
    int power;
    int torque;

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

    public int getPower() {
        return power;
    }

    public void setPower(int power) {
        this.power = power;
    }

    public int getTorque() {
        return torque;
    }

    public void setTorque(int torque) {
        this.torque = torque;
    }
}
