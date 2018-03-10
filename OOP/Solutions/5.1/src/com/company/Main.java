package com.company;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        char c;
        String name;
        Scanner in = new Scanner(System.in);
        MyCollection<Rank> collection = new MyCollection<>();

        while (true) {
            System.out.println("Would You like to add private (p), corporal (c), sergeant (s) or warrant officer (any other char)?");
            c = in.next().charAt(0);
            System.out.println("Type his name:");
            name = in.next();

            if (c == 'p')
                collection.add(new Private(name));
            else if (c == 'c')
                collection.add(new Corporal(name));
            else if (c == 's')
                collection.add(new Sergeant(name));
            else
                collection.add(new WarrantOfficer(name));

            System.out.println("Would You like to add any other guy? (y or n)");
            c = in.next().charAt(0);
            if (c == 'n')
                break;
        }

        collection.printAll();

        MyCollection.Elem e = collection.first;

        while (e != null) {
            System.out.println(e);
            e = e.next;
        }
    }
}
