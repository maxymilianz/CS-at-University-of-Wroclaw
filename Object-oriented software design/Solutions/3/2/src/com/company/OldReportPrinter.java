package com.company;

public class OldReportPrinter {
    private String data;

    public OldReportPrinter(String data) {
        this.data = data;
    }

    public void formatDocument() {
        // some implementation
    }

    public void printReport() {
        System.out.println(data);
    }

    public String getData() {
        return data;
    }
}
