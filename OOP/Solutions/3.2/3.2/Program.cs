using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _3._2 {
    class Program {
        static void Main(string[] args) {
            Console.WriteLine("What key would You like to initialize the dictionary?");
            int key = int.Parse(Console.ReadLine());

            Console.WriteLine("What value would You like to initialize the dictionary?");
            string val = Console.ReadLine();

            Dictionary<int, string> dict = new Dictionary<int, string>(key, val);

            Console.WriteLine("How many entries would You like to add?");
            int count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the key:");
                key = int.Parse(Console.ReadLine());
                Console.WriteLine("Type the value:");
                val = Console.ReadLine();

                dict.add(key, val);
            }

            Console.WriteLine("How many entries would You like to look for?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the key:");
                key = int.Parse(Console.ReadLine());
                Console.WriteLine(dict.search(key).Val);
            }

            Console.WriteLine("How many entries would You like to delete?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the key:");
                key = int.Parse(Console.ReadLine());
                dict.delete(key);
            }
        }
    }

    public class Dictionary<K, V> {
        public class Elem<K, V> {
            K key;
            V val;
            Elem<K, V> next;
            Elem<K, V> prev;

            public Elem(K key, V val) {
                this.key = key;
                this.val = val;
                next = null;
                prev = null;
            }

            public K Key {
                get {
                    return key;
                }
            }

            public V Val {
                get {
                    return val;
                }
            }

            public Elem<K, V> Prev {
                get {
                    return prev;
                }

                set {
                    prev = value;
                }
            }

            public Elem<K, V> Next {
                get {
                    return next;
                }

                set {
                    next = value;
                }
            }
        }

        Elem<K, V> last;

        public Dictionary(K key, V val) {
            last = new Elem<K, V>(key, val);
        }

        public void add(K key, V val) {
            if (last == null)
                last = new Elem<K, V>(key, val);
            else {
                last.Next = new Elem<K, V>(key, val);
                last.Next.Prev = last;
                last = last.Next;
            }
        }

        public Elem<K, V> search(K key) {
            Elem<K, V> e = last;

            while (e != null && !e.Key.Equals(key)) {
                e = e.Prev;
            }

            if (e == null)
                return new Elem<K, V>(key, default(V));
            else
                return e;
        }

        public void delete(K key) {
            Elem<K, V> e = search(key);
            
            if (e.Next != null)
                e.Next.Prev = e.Prev;
            if (e.Prev != null)
                e.Prev.Next = e.Next;
        }
    }
}
