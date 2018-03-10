package com.company;

import java.io.*;

/**
 * Created by Lenovo on 06.04.2017.
 */
public class Vehicle implements Serializable {
    public String manufacturer, model;
    public int maxSpeed;
    public double acc0To100;

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
}
