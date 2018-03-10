package com.company;

import java.io.*;

/**
 * Created by Lenovo on 08.04.2017.
 */
public class TramSerialization {
    String filename;

    public TramSerialization(String filename) {
        this.filename = filename;
    }

    public void serialize(Tram vehicle) {
        try {
            FileOutputStream fileOut = new FileOutputStream(filename);
            ObjectOutputStream objOut = new ObjectOutputStream(fileOut);
            objOut.writeObject(vehicle);
            objOut.close();
            fileOut.close();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Tram deserialize() {
        try {
            File file = new File(filename);
            Tram v = new Tram();

            if (file.isDirectory()) {
                System.out.println("This is a directory!");
                System.exit(1);
            }
            else if (file.exists()) {
                FileInputStream fileIn = new FileInputStream(filename);
                ObjectInputStream objIn = new ObjectInputStream(fileIn);
                v = (Tram) objIn.readObject();
                objIn.close();
                fileIn.close();
            }

            return v;
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
