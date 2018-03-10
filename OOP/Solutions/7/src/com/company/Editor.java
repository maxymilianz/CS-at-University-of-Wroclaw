package com.company;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by Lenovo on 07.04.2017.
 */
public class Editor extends JPanel {
    class Listener implements ActionListener {
        ArrayList<JTextField> list;

        Listener(ArrayList<JTextField> list) {
            this.list = list;
        }

        public void actionPerformed(ActionEvent e) {
            if (e.getActionCommand().equals("save")) {
                for (int i = 0; i < fields.size(); i++) {
                    try {
                        if (fields.get(i).getType().toString().equals("int"))
                            object.getClass().getField(fields.get(i).getName()).set(object, Integer.parseInt(list.get(i).getText()));
                        else if (fields.get(i).getType().toString().equals("double"))
                            object.getClass().getField(fields.get(i).getName()).set(object, Double.parseDouble(list.get(i).getText()));
                        else
                            object.getClass().getField(fields.get(i).getName()).set(object, list.get(i).getText());
                    }
                    catch (Exception exception) {
                        exception.printStackTrace();
                    }
                }
            }

            serialization.serialize(object);
            System.exit(1);
        }
    }

    Object object;
    Serialization serialization;
    ArrayList<Field> fields = new ArrayList<>();

    public Editor(Object o, Serialization s) {
        object = o;
        serialization = s;
        Class c = o.getClass();

        while (c != null) {
            fields.addAll(Arrays.asList(c.getDeclaredFields()));
            c = c.getSuperclass();
        }

        GridLayout layout = new GridLayout();
        layout.setColumns(2);
        layout.setRows(fields.size() + 1);
        this.setLayout(layout);

        addComponents();
    }

    void addComponents() {
        ArrayList<JTextField> list = new ArrayList<>();

        for (int i = 0; i < fields.size(); i++) {
            this.add(new JLabel(fields.get(i).getName()));

            try {
                JTextField field = new JTextField(fields.get(i).get(object).toString());
                list.add(field);
                this.add(field);
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        JButton save = new JButton("save");
        JButton cancel = new JButton("cancel");

        Listener listener = new Listener(list);

        save.addActionListener(listener);
        cancel.addActionListener(listener);

        this.add(save);
        this.add(cancel);
    }
}
