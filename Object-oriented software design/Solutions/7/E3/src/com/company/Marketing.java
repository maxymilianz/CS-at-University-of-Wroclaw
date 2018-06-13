package com.company;

class Marketing extends AbstractHandler {
    Marketing() {

    }

    Marketing(AbstractHandler next) {
        this.next = next;
    }

    @Override
    void handle(String mail) {
        if (mail.charAt(0) == 'D')
            readAndReact(mail);
        else if (next != null)
            next.handle(mail);
    }

    private void readAndReact(String mail) {
        System.out.println("Oh, it's some mail.");
    }
}
