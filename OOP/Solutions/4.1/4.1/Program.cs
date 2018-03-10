using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _4._1 {
    class Program {
        static void Main(string[] args) {
            // LISTA=========================================================================================================================================================

            Console.WriteLine("What value would You like to initialize the list?");
            int val = int.Parse(Console.ReadLine());

            Lista<int> list = new Lista<int>(val);

            Console.WriteLine("How many elements would You like to add to the start of the list?");
            int count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the {0}. element:", i);
                val = int.Parse(Console.ReadLine());
                list.dodajNaPocz(val);
            }

            Console.WriteLine("How many elements would You like to add to the end of the list?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the {0}. element:", i);
                val = int.Parse(Console.ReadLine());
                list.dodajNaKon(val);
            }

            Console.WriteLine("How many elements would You like to display?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Which element would You like to display?");
                val = int.Parse(Console.ReadLine());
                Console.WriteLine("{0}. element: {1}", val, list[val]);
            }

            Console.WriteLine("How many elements would You like to check if exist in the list?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Which element would You like to check?");
                val = int.Parse(Console.ReadLine());
                Console.WriteLine(list.present(val));
            }

            Console.WriteLine("All the elements:");
            foreach (int i in list)
                Console.WriteLine(i);

            // DICTIONARY====================================================================================================================================================

            Console.WriteLine("What key would You like to initialize the dictionary?");
            int key = int.Parse(Console.ReadLine());

            Console.WriteLine("What value would You like to initialize the dictionary?");
            string stringVal = Console.ReadLine();

            Dictionary<int, string> dict = new Dictionary<int, string>(key, stringVal);

            Console.WriteLine("How many entries would You like to add?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Type the key:");
                key = int.Parse(Console.ReadLine());
                Console.WriteLine("Type the value:");
                stringVal = Console.ReadLine();

                dict.add(key, stringVal);
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

            Console.WriteLine("How many elements would You like to check if exist in the dictionary? (By value, not key)");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++) {
                Console.WriteLine("Which element would You like to check?");
                stringVal = Console.ReadLine();
                Console.WriteLine(dict.present(stringVal));
            }

            Console.WriteLine("How many elements would You like to delete from the start of the dictionary?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++)
                dict.deleteFirst();

            Console.WriteLine("How many elements would You like to delete from the end of the dictionary?");
            count = int.Parse(Console.ReadLine());

            for (int i = 0; i < count; i++)
                dict.deleteLast();
        }
    }

    interface ISimpleCollections<T> {
        void deleteFirst();
        void deleteLast();
        bool present(T val);
    }

    public class Elem<T> {
        bool czyNull = false;
        T wart;
        Elem<T> nast;
        Elem<T> poprz;

        public Elem() {
            this.czyNull = true;
            this.nast = null;
            this.poprz = null;
        }

        public Elem(T wart) {
            this.wart = wart;
            this.nast = null;
            this.poprz = null;
        }

        public void dodajPrzed(T wart) {
            this.poprz = new Elem<T>(wart);
            this.poprz.nast = this;
            this.poprz.poprz = null;
        }

        public void dodajZa(T wart) {
            this.nast = new Elem<T>(wart);
            this.nast.nast = null;
            this.nast.poprz = this;
        }

        public T this[int index] {
            get {
                if (index == 0)
                    return wart;
                else {
                    if (nast != null)
                        return nast[--index];
                    else
                        return default(T);
                }
            }
        }

        public Elem<T> wezPoprz() {
            return this.poprz;
        }

        public Elem<T> wezNast() {
            return this.nast;
        }

        public T Wart {
            get {
                return wart;
            }
        }

        public void wypisz() {
            if (!czyNull)
                Console.WriteLine(wart);
            else
                Console.WriteLine("Nie ma takiego elementu!");
        }

        public string ToString() {
            return this.wart.ToString();
        }
    }

    public class Lista<T> : IEnumerable<T>, ISimpleCollections<T> {
        int length;
        Elem<T> pocz;
        Elem<T> kon;

        public Lista(T inicj) {
            length = 1;
            pocz = new Elem<T>(inicj);
            kon = pocz;
        }

        public void dodajNaPocz(T e) {
            length++;

            if (pocz != null) {
                pocz.dodajPrzed(e);
                pocz = pocz.wezPoprz();
            }
            else {
                pocz = new Elem<T>(e);
                kon = pocz;
            }
        }

        public void dodajNaKon(T e) {
            length++;

            if (kon != null) {
                kon.dodajZa(e);
                kon = kon.wezNast();
            }
            else {
                kon = new Elem<T>(e);
                pocz = kon;
            }
        }

        public Elem<T> usunPocz() {
            length -= length < 0 ? 0 : 1;
            Elem<T> temp = pocz;

            if (this != null) {
                if (pocz != kon)
                    pocz = pocz.wezNast();
                else {
                    pocz = null;
                    kon = null;
                }
            }

            if (temp != null)
                return temp;
            else
                return new Elem<T>();
        }

        public Elem<T> usunKon() {
            length -= length < 0 ? 0 : 1;
            Elem<T> temp = kon;

            if (this != null) {
                if (pocz != kon)
                    kon = kon.wezPoprz();
                else {
                    pocz = null;
                    kon = null;
                }
            }

            if (temp != null)
                return temp;
            else
                return new Elem<T>();
        }

        public IEnumerator<T> GetEnumerator() {
            return new ListaEnumerator<T>(this);
        }

        IEnumerator IEnumerable.GetEnumerator() {
            return GetEnumerator();
        }

        public void deleteFirst() {
            usunPocz();
        }

        public void deleteLast() {
            usunKon();
        }

        public bool present(T val) {
            Elem<T> temp = pocz;

            while (temp != null && !temp.Wart.Equals(val))
                temp = temp.wezNast();
            if (temp != null)
                return true;
            else
                return false;
        }

        public T this[int index] {
            get {
                return pocz[index];
            }
        }

        public int Length {
            get {
                return length;
            }
        }

        public Elem<T> Pocz {
            get {
                return pocz;
            }
        }
    }

    public class ListaEnumerator<T> : IEnumerator<T> {
        Lista<T> list;
        Elem<T> current;

        public ListaEnumerator(Lista<T> val) {
            list = val;
            current = null;
        }

        public T Current {
            get {
                return current.Wart;
            }
        }

        object IEnumerator.Current {
            get {
                return Current;
            }
        }

        public void Dispose() { }

        public bool MoveNext() {
            if (current == null) {
                current = list.Pocz;
                return current != null;
            }

            if (current.wezNast() != null) {
                current = current.wezNast();
                return true;
            }
            else
                return false;
        }

        public void Reset() {
            current = null;
        }
    }

    public class Dictionary<K, V> : ISimpleCollections<V> {
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

        public void deleteFirst() {
            Elem<K, V> temp = last;

            while (temp.Prev != null)
                temp = temp.Prev;

            delete(temp.Key);
        }

        public void deleteLast() {
            delete(last.Key);
        }

        public bool present(V val) {
            Elem<K, V> temp = last;

            while (temp != null && !temp.Val.Equals(val))
                temp = temp.Prev;
            if (temp != null)
                return true;
            else
                return false;
        }
    }
}
