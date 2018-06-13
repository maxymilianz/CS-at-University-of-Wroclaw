package com.company;

public class Main {

    public static void main(String[] args) {
        AbstractHandler handler = new Archivizer("C:\\Users\\Maksymilian Zawartko\\Documents\\Dokumenty\\studia\\lato 17-18\\POO\\7\\E3\\archive.txt",
                new President(new LegalDepartment(new Sales(new Marketing()))));
        handler.handle("D");
    }
}
