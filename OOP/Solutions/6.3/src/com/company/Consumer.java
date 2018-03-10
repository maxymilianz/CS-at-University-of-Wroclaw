package com.company;

/**
 * Created by Lenovo on 01.04.2017.
 */
public class Consumer implements Runnable {
    public void run() {
        while (true) {
            try {
                System.out.println(Main.buffer.get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
