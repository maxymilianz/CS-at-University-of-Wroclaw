using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _4._2 {
    class Program {
        static void Main(string[] args) {
            Console.WriteLine("How many primes do You want to generate? (Without displaying them!)");
            int count = int.Parse(Console.ReadLine());

            PrimeCollection collection = new PrimeCollection(count);

            Console.WriteLine("Which prime do You want to display?");
            count = int.Parse(Console.ReadLine());

            Console.WriteLine(collection[count]);

            Console.WriteLine("Type anything, when You are ready to display all the primes in the int range.");
            Console.Read();

            foreach (int i in collection)
                Console.WriteLine(i);
        }
    }

    public class PrimeCollection : IEnumerable {
        class Elem {
            int val = 0;
            Elem next = null;
            Elem prev = null;

            public Elem() {
                val = 2;
            }

            public Elem(int value) {
                val = value;
            }

            public int this[int i] {
                get {
                    if (i == 0)
                        return this.val;
                    else
                        return this.next[--i];
                }
            }

            public int Val {
                get {
                    return val;
                }
                set {
                    val = value;
                }
            }

            public Elem Next {
                get {
                    return next;
                }
                set {
                    next = value;
                }
            }

            public Elem Prev {
                get {
                    return prev;
                }
                set {
                    prev = value;
                }
            }
        }

        int count = 0;
        Elem first = null;
        Elem last = null;

        public PrimeCollection() { }

        public PrimeCollection(int iter) {
            first = new Elem();
            last = first;

            for (count = 1; count < iter; count++) {
                int n = last.Val + 1;

                for (int i = 0; i < count; i++) {
                    if (n % first[i] == 0) {
                        n++;
                        i = -1;
                    }
                }

                if (n > 0) {
                    last.Next = new Elem(n);
                    last.Next.Prev = last;
                    last = last.Next;
                }
                else
                    break;
            }
        }

        public int LastVal {
            get {
                return last.Val;
            }
        }

        public int getNext() {
            count++;
            int n = last.Val + 1;

            /*for (int i = 0; first[i] < last.Val; i++) {
                if (n % first[i] == 0) {
                    n++;
                    i = -1;
                }
            }*/

            bool found = false;

            /*while (!found) {
                found = true;
                foreach (int i in this) {
                    if (n % i == 0) {
                        found = false;
                        n++;
                        break;
                    }
                }
            }*/

            while (!found) {
                found = true;
                Elem temp = first;
                while (temp != null) {
                    if (n % temp.Val == 0) {
                        found = false;
                        n++;
                        break;
                    }

                    temp = temp.Next;
                }
            }

            if (n > 0) {
                last.Next = new Elem(n);
                last.Next.Prev = last;
                last = last.Next;
            }
            else
                Environment.Exit(1);

            return last.Val;
        }

        public int this[int i] {
            get {
                while (i >= count)
                    getNext();

                return first[i];
            }
        }

        public IEnumerator GetEnumerator() {
            return new PrimeCollectionEnumerator(this);
        }
    }

    public class PrimeCollectionEnumerator : IEnumerator {
        int pos = -1;
        PrimeCollection collection;

        public PrimeCollectionEnumerator(PrimeCollection val) {
            collection = val;
        }

        public object Current {
            get {
                return collection[pos];
            }
        }

        public bool MoveNext() {
            pos++;

            if (collection.LastVal > 0)
                return true;
            else
                return false;
        }

        public void Reset() {
            pos = -1;
        }
    }
}
