package com.company;

import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("How long do You want the list to be?");
        Scanner in = new Scanner(System.in);
        int length = in.nextInt();
        String names[] = new String[length];
        Buffer<String> buffer = new Buffer<>(length);

        System.out.println("Do You want to enter names (n) or generate random strings (r)?");
        char choice = in.next().charAt(0);

        if (choice == 'n') {
            for (int i = 0; i < length; i++) {
                System.out.println("Enter " + i + ". name:");
                names[i] = in.next();
            }
        }
        else {
            String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            Random r = new Random();

            for (int i = 0; i < length; i++) {
                int size = r.nextInt(50);
                StringBuilder sb = new StringBuilder();

                for (int j = 0; j < size; j++) {
                    int rand = r.nextInt(25);
                    sb.append(chars.charAt(rand));
                }

                names[i] = sb.toString();
            }
        }

        System.out.println("What prefix do You want to look for?");
        Thread filter = new Thread(new Filter(in.next(), names, buffer));
        Thread sorter = new Thread(new Sorter(buffer));

        filter.start();
        sorter.start();
    }
}
