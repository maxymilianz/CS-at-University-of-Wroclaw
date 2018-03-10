package com.company;

import java.util.HashMap;
import java.util.Scanner;

public class Main {
    static Scanner in = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("How many variables will You be willing to create?");
        int count = in.nextInt();
        Expression.map = new HashMap<>(count);

        System.out.println("Would You like to create addition (a), subtraction (s), multiplication (m), division (d), a number (n) or a variable (v)?");
        char t = in.next().charAt(0);

        Expression e = addExpression(t);

        System.out.println(e.toString() + " = " + e.value());
    }

    static Expression addExpression(char type) {
        if (type == 'n') {
            System.out.println("Type the number:");
            double n = in.nextDouble();
            return new Constant(n);
        }
        else if (type == 'v') {
            System.out.println("Type the name of the variable:");
            String name = in.next();
            System.out.println("Type the value of the variable:");
            double value = in.nextDouble();

            Expression.map.put(name, value);
            return new Variable(name);
        }
        else {
            System.out.println("Would You like the first element be addition (a), subtraction (s), multiplication (m), division (d), a number (n) or a variable (v)?");
            char l = in.next().charAt(0);
            System.out.println("Would You like the second element be addition (a), subtraction (s), multiplication (m), division (d), a number (n) or a variable (v)?");
            char r = in.next().charAt(0);

            if (type == 'a')
                return new Addition(addExpression(l), addExpression(r));
            else if (type == 's')
                return new Subtraction(addExpression(l), addExpression(r));
            else if (type == 'm')
                return new Multiplication(addExpression(l), addExpression(r));
            else if (type == 'd')
                return new Division(addExpression(l), addExpression(r));
            else
                return null;
        }
    }
}
