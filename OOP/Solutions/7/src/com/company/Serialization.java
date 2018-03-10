package com.company;

import java.io.*;

/**
 * Created by Lenovo on 07.04.2017.
 */
public class Serialization {
    String className, filename;

    public Serialization(String className, String filename) {
        this.className = className;
        this.filename = filename;
    }

    public void serialize(Object o) {
        try {
            FileOutputStream fileOut = new FileOutputStream(filename);
            ObjectOutputStream objOut = new ObjectOutputStream(fileOut);
            objOut.writeObject(o);
            objOut.close();
            fileOut.close();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Object deserialize() {
        File file = new File(filename);
        Object o = new Object();

        if (file.isDirectory()) {
            System.out.println("This is a directory!");
            System.exit(1);
        }
        else if (file.exists()) {
            try {
                FileInputStream fileIn = new FileInputStream(filename);
                ObjectInputStream objIn = new ObjectInputStream(fileIn);
                o = (Class.forName("com.company." + className)).cast(objIn.readObject());
                objIn.close();
                fileIn.close();
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
        else {
            try {
                o = Class.forName("com.company." + className).newInstance();
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        return o;
    }
}
