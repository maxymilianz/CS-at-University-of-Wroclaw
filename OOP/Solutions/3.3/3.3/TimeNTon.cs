using System;
using System.Collections.Generic;

namespace TNTNamespace {
    public sealed class TimeNTon {
        const int N = 3;

        public static DateTime start = new DateTime(2017, 3, 17, 8, 0, 0);
        //static DateTime start = DateTime.Now.AddHours(-1);
        static DateTime end = start.AddHours(2);

        static int i = -1;
        static List<TimeNTon> instances = new List<TimeNTon>();
        int id;

        TimeNTon() {
            id = -1;
        }

        TimeNTon(int i) {
            id = i;
        }

        public int getId() {
            return id;
        }

        public static TimeNTon instance() {
            if (DateTime.Now.CompareTo(start) == 1 && DateTime.Now.CompareTo(end) == -1) {
                if (instances.Count == TimeNTon.N) {
                    i++;
                    if (i == TimeNTon.N)
                        i = 0;
                    return instances[i];
                }
                else {
                    instances.Add(new TimeNTon(instances.Count));
                    return instances[instances.Count - 1];
                }
            }
            else {
                if (instances.Count == 0)
                    return new TimeNTon();
                else
                    return instances[0];
            }
        }
    }
}