package com.company;

import javafx.geometry.Point2D;

import java.util.LinkedList;
import java.util.Random;

public class Main {

    public static void main(String[] args) {
        Factory factory = new Factory();
        for (int i = 0; i < 4; i++)
            System.out.println(factory.makeProduct().getId());

        Square square = new Square(new Point2D(1, 2), new Point2D(2, 3), new Point2D(9, 8), new Point2D(8, 7));
        square.print();
        Circle circle = new Circle(new Point2D(4, 5), 4.5f);
        circle.print();

        Encryptor encryptor = new Encryptor();
        int[] a = {1, 8192, 2137};
        for (int n : encryptor.encryptArray(a))
            System.out.println(n);
        LinkedList<Integer> l = new LinkedList<>();
        l.add(2000000);
        l.add(1997);
        l.add(15);
        for (int n : encryptor.encryptList(l))
            System.out.println(n);

        Key key = new Key(new Random().nextInt());
        Car car = new Car(key);
        System.out.println(car.isOpened());
        car.open(key);
        System.out.println(car.isOpened());
        car.close(key);
        System.out.println(car.isOpened());

        Worker worker = new Worker(968);
        System.out.println(worker.isMachineOn());
        worker.turnOnMachine();
        System.out.println(worker.isMachineOn());
        worker.turnOffMachine();
        System.out.println(worker.isMachineOn());
        worker.turnOnMachine();
    }
}
