package com.company;

public class Main {

    public static void main(String[] args) {
        Report report = new Report("foobar");
        new ReportPrinter().printReport(report);

        OldReportPrinter printer = new OldReportPrinter("foobaz");
        printer.printReport();
    }
}
