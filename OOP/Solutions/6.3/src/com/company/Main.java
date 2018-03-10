package com.company;

import java.util.Scanner;

public class Main {
    public static Buffer<String> buffer;

    public static void main(String[] args) {
        System.out.println("How long do You want the buffer to be?");
        Scanner in = new Scanner(System.in);
        int size = in.nextInt();
        buffer = new Buffer<>(size);

        Thread producer = new Thread(new Producer());
        Thread consumer = new Thread(new Consumer());

        producer.start();
        consumer.start();
    }
}
