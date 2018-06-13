package com.company;

import java.util.LinkedList;
import java.util.Random;

/*
Protected Variations - encryption algorithm may change in the future, so I make it a method instead of XORing every int
in encryptArray and encryptList separately
 */

public class Encryptor {
    private int mask;

    public Encryptor() {
        mask = new Random().nextInt();
    }

    private int encrypt(int n) {
        return n ^ mask;
    }

    public int[] encryptArray(int[] a) {
        int[] result = new int[a.length];

        for (int i = 0; i < result.length; i++)
            result[i] = encrypt(a[i]);

        return result;
    }

    public LinkedList<Integer> encryptList(LinkedList<Integer> l) {
        LinkedList<Integer> result = new LinkedList<>();

        for (int n : l) {
            result.add(encrypt(n));
        }

        return result;
    }
}
