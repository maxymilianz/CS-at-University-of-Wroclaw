package com.company;

import javax.swing.*;
import java.awt.*;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Enter the name of the file from which You would like to deserialize an object:");
        Scanner in = new Scanner(System.in);
        String filename = in.next();
        System.out.println("Enter the name of the class of this object:");
        String className = in.next();

        Serialization serialization = new Serialization(className, filename);
        Object o = serialization.deserialize();

        JFrame frame = new JFrame(className + " editor");
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        Container container = frame.getContentPane();

        Editor editor = new Editor(o, serialization);
        container.add(editor);

        frame.pack();
        frame.setVisible(true);
    }
}
