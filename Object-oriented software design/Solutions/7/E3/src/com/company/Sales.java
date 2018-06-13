package com.company;

class Sales extends AbstractHandler {
    Sales() {

    }

    Sales(AbstractHandler next) {
        this.next = next;
    }

    @Override
    void handle(String mail) {
        if (mail.charAt(0) == 'O')
            readAndReact(mail);
        else if (next != null)
            next.handle(mail);
    }

    private void readAndReact(String mail) {
        System.out.println("Oh, it's an order.");
    }
}
