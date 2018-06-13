package com.company;

import java.lang.reflect.Type;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.List;

class EventAggregator {
    private static EventAggregator instance = new EventAggregator();

    private Hashtable<Type, List<Subscriber>> subscribers;

    private EventAggregator() {
        subscribers = new Hashtable<>();
    }

    void addSubscriber(Subscriber subscriber) {
        for (Type type : subscriber.getNotificationTypes()) {
            if (!subscribers.containsKey(type))
                subscribers.put(type, new LinkedList<>());

            subscribers.get(type).add(subscriber);
        }
    }

    void removeSubscriber(Subscriber subscriber) {
        for (Type type : subscriber.getNotificationTypes()) {
            if (subscribers.containsKey(type))
                subscribers.get(type).remove(subscriber);
        }
    }

    void publish(Notification notification) {
        Type type = notification.getClass();

        if (subscribers.containsKey(type))
            for (Subscriber subscriber : subscribers.get(type))
                subscriber.handle(notification);
    }

    static EventAggregator getInstance() {
        return instance;
    }
}
