package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

/**
 * Created by Lenovo on 08.04.2017.
 */
public class VehicleEditor extends JPanel {
    class Listener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (e.getActionCommand().equals("Save")) {
                vehicle.setManufacturer(table.get("manufacturer").getText());
                vehicle.setModel(table.get("model").getText());
                vehicle.setMaxSpeed(Integer.parseInt(table.get("maxSpeed").getText()));
                vehicle.setAcc0To100(Double.parseDouble(table.get("acc0to100").getText()));
                serialization.serialize(vehicle);
            }

            System.exit(1);
        }
    }

    Vehicle vehicle;
    VehicleSerialization serialization;
    Hashtable<String, JTextField> table;

    public VehicleEditor(Vehicle vehicle, VehicleSerialization serialization) {
        this.vehicle = vehicle;
        this.serialization = serialization;
        table = new Hashtable<>();

        table.put("manufacturer", new JTextField(vehicle.getManufacturer()));
        table.put("model", new JTextField(vehicle.getModel()));
        table.put("maxSpeed", new JTextField(Integer.toString(vehicle.getMaxSpeed())));
        table.put("acc0to100", new JTextField(((Double) vehicle.getAcc0To100()).toString()));

        this.setLayout(new GridLayout(table.size() + 1, 2));

        this.add(new JLabel("Manufacturer: "));
        this.add(table.get("manufacturer"));
        this.add(new JLabel("Model: "));
        this.add(table.get("model"));
        this.add(new JLabel("Max. speed: "));
        this.add(table.get("maxSpeed"));
        this.add(new JLabel("Acceleration 0-100 kmph: "));
        this.add(table.get("acc0to100"));

        JButton save = new JButton("Save");
        JButton cancel = new JButton("Cancel");
        this.add(save);
        this.add(cancel);
        Listener listener = new Listener();
        save.addActionListener(listener);
        cancel.addActionListener(listener);
    }
}
