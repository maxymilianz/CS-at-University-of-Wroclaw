package com.company;

class President extends AbstractHandler {
    President() {

    }

    President(AbstractHandler next) {
        this.next = next;
    }

    @Override
    void handle(String mail) {
        if (mail.charAt(0) == 'P')
            readAndReact(mail);
        else if (next != null)
            next.handle(mail);
    }

    private void readAndReact(String mail) {
        System.out.println("Oh, it's a praising letter.");
    }
}
