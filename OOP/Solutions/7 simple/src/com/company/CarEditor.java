package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;

/**
 * Created by Lenovo on 08.04.2017.
 */
public class CarEditor extends JPanel {
    class Listener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (e.getActionCommand().equals("Save")) {
                vehicle.setManufacturer(table.get("manufacturer").getText());
                vehicle.setModel(table.get("model").getText());
                vehicle.setMaxSpeed(Integer.parseInt(table.get("maxSpeed").getText()));
                vehicle.setAcc0To100(Double.parseDouble(table.get("acc0to100").getText()));
                vehicle.setPower(Integer.parseInt(table.get("power").getText()));
                vehicle.setTorque(Integer.parseInt(table.get("torque").getText()));
                serialization.serialize(vehicle);
            }

            System.exit(1);
        }
    }

    Car vehicle;
    CarSerialization serialization;
    Hashtable<String, JTextField> table;

    public CarEditor(Car vehicle, CarSerialization serialization) {
        this.vehicle = vehicle;
        this.serialization = serialization;
        table = new Hashtable<>();

        table.put("manufacturer", new JTextField(vehicle.getManufacturer()));
        table.put("model", new JTextField(vehicle.getModel()));
        table.put("maxSpeed", new JTextField(Integer.toString(vehicle.getMaxSpeed())));
        table.put("acc0to100", new JTextField(((Double) vehicle.getAcc0To100()).toString()));
        table.put("power", new JTextField(Integer.toString(vehicle.getPower())));
        table.put("torque", new JTextField(Integer.toString(vehicle.getTorque())));

        this.setLayout(new GridLayout(table.size() + 1, 2));

        this.add(new JLabel("Manufacturer: "));
        this.add(table.get("manufacturer"));
        this.add(new JLabel("Model: "));
        this.add(table.get("model"));
        this.add(new JLabel("Max. speed: "));
        this.add(table.get("maxSpeed"));
        this.add(new JLabel("Acceleration 0-100 kmph: "));
        this.add(table.get("acc0to100"));
        this.add(new JLabel("Power: "));
        this.add(table.get("power"));
        this.add(new JLabel("Torque: "));
        this.add(table.get("torque"));

        JButton save = new JButton("Save");
        JButton cancel = new JButton("Cancel");
        this.add(save);
        this.add(cancel);
        Listener listener = new Listener();
        save.addActionListener(listener);
        cancel.addActionListener(listener);
    }
}
