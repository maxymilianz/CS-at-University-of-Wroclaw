package com.company;

import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class Archivizer extends AbstractHandler {
    private Path path;

    Archivizer(String path) {
        this.path = FileSystems.getDefault().getPath(path);
    }

    Archivizer(String path, AbstractHandler next) {
        this.path = FileSystems.getDefault().getPath(path);
        this.next = next;
    }

    @Override
    void handle(String mail) {
        try {
            Files.write(path, (mail + '\n').getBytes(), StandardOpenOption.APPEND, StandardOpenOption.CREATE);
            if (next != null)
                next.handle(mail);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
