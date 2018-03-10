package com.company;

import java.util.Random;

/**
 * Created by Lenovo on 01.04.2017.
 */
public class Producer implements Runnable {
    String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    Random random = new Random();

    String generate() {
        int size = random.nextInt(50);
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < size; i++) {
            int rand = random.nextInt(25);
            sb.append(chars.charAt(rand));
        }

        return sb.toString();
    }

    public void run() {
        while (true) {
            try {
                Main.buffer.add(generate());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
