package com.company;

import java.lang.reflect.Type;
import java.util.Set;

interface Subscriber {
    void handle(Notification notification);

    Set<Type> getNotificationTypes();
}
