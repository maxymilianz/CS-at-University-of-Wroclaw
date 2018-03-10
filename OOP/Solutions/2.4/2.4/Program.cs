using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _2._4 {
    class Program {
        static void Main(string[] args) {
            int tn;
            int e;
            ListaLeniwa l = new ListaLeniwa();
            Pierwsze p = new Pierwsze();

            Console.WriteLine("Ktory element leniwej listy wyswietlic?");
            e = int.Parse(Console.ReadLine());
            Console.WriteLine(l.element(e));

            Console.WriteLine("Czy chcesz wyswietlic jeszcze jakis element? (1 / 0)");
            tn = int.Parse(Console.ReadLine());
            if (tn == 1) {
                Console.WriteLine("Ktory element leniwej listy wyswietlic?");
                e = int.Parse(Console.ReadLine());
                Console.WriteLine(l.element(e));
            }

            Console.WriteLine("Rozmiar listy leniwej: {0}", l.size());

            Console.WriteLine("Ktory element listy liczb pierwszych wyswietlic?");
            e = int.Parse(Console.ReadLine());
            Console.WriteLine(p.element(e));

            Console.WriteLine("Czy chcesz wyswietlic jeszcze jakis element? (1 / 0)");
            tn = int.Parse(Console.ReadLine());
            if (tn == 1) {
                Console.WriteLine("Ktory element listy liczb pierwszych wyswietlic?");
                e = int.Parse(Console.ReadLine());
                Console.WriteLine(p.element(e));
            }

            Console.WriteLine("Rozmiar listy liczb pierwszych: {0}", p.size());
        }
    }

    class ListaLeniwa {
        protected List<int> l = new List<int>();

        protected virtual int add(int i) {
            if (i == -1)
                return 0;

            return l[i] + 1;
        }

        public int element(int i) {
            if (l.Count == 0)
                l.Add(add(-1));

            for (int j = l[l.Count - 1]; l.Count <= i && j >= 0; j++)
                l.Add(add(j));

            return l[i];
        }

        public int size() {
            return l.Count;
        }
    }

    class Pierwsze : ListaLeniwa {
        protected override int add(int i) {
            if (i == -1)
                return 2;

            bool cont = true;

            while (cont) {
                cont = false;
                i++;

                for (int k = 0; k < l.Count; k++)
                    if (i % l[k] == 0) {
                        cont = true;
                        break;
                    }
            }

            return i;
        }
    }
}
