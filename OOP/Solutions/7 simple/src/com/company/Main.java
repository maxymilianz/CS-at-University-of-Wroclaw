package com.company;

import javax.swing.*;
import java.awt.*;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        System.out.println("Enter filename:");
        Scanner in = new Scanner(System.in);
        String filename = in.next();

        System.out.println("Enter class name:");
        String className = in.next();

        JFrame frame = new JFrame("Editor");
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        Container c = frame.getContentPane();

        if (className.equals("Vehicle")) {
            VehicleSerialization serialization = new VehicleSerialization(filename);
            Vehicle o = serialization.deserialize();
            c.add(new VehicleEditor(o, serialization));
        }
        else if (className.equals("Car")) {
            CarSerialization serialization = new CarSerialization(filename);
            Car o = serialization.deserialize();
            c.add(new CarEditor(o, serialization));
        }
        else {
            TramSerialization serialization = new TramSerialization(filename);
            Tram o = serialization.deserialize();
            c.add(new TramEditor(o, serialization));
        }

        frame.pack();
        frame.setVisible(true);
    }
}
