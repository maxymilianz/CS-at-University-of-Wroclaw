package com.company;

class LegalDepartment extends AbstractHandler {
    LegalDepartment() {

    }

    LegalDepartment(AbstractHandler next) {
        this.next = next;
    }

    @Override
    void handle(String mail) {
        if (mail.charAt(0) == 'C')
            readAndReact(mail);
        else if (next != null)
            next.handle(mail);
    }

    private void readAndReact(String mail) {
        System.out.println("Oh, it's a complaint.");
    }
}
