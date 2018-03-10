package com.company;

import java.io.*;

/**
 * Created by Lenovo on 06.04.2017.
 */
public class Vehicle implements Serializable {
    String manufacturer, model;
    int maxSpeed;
    double acc0To100;

    public Vehicle() {
        manufacturer = "";
        model = "";
        maxSpeed = 0;
        acc0To100 = 0;
    }

    /*public Vehicle(String manufacturer, String model, int maxSpeed, double acc0To100) {
        this.manufacturer = manufacturer;
        this.model = model;
        this.maxSpeed = maxSpeed;
        this.acc0To100 = acc0To100;
    }*/

    public String toString() {
        return manufacturer + " " + model + ", max. speed: " + maxSpeed + ", acceleration 0-100: " + acc0To100;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public int getMaxSpeed() {
        return maxSpeed;
    }

    public void setMaxSpeed(int maxSpeed) {
        this.maxSpeed = maxSpeed;
    }

    public double getAcc0To100() {
        return acc0To100;
    }

    public void setAcc0To100(double acc0To100) {
        this.acc0To100 = acc0To100;
    }
}
