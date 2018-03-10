using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using ListaNamespace;

namespace _3._1 {
    class Program {
        static void Main(string[] args) {
            Console.WriteLine("Jaka wartoscia zainicjalizowac liste?");
            int wart = int.Parse(Console.ReadLine());
            Lista<int> l = new Lista<int>(wart);

            Console.WriteLine("Ile elementow chcesz dodac na poczatek listy?");
            int ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++) {
                Console.WriteLine("Podaj {0} element:", i + 1);
                wart = int.Parse(Console.ReadLine());
                l.dodajNaPocz(wart);
            }

            Console.WriteLine("Ile elementow chcesz dodac na koniec listy?");
            ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++) {
                Console.WriteLine("Podaj {0} element:", i + 1);
                wart = int.Parse(Console.ReadLine());
                l.dodajNaKon(wart);
            }

            Console.WriteLine("Ile elementow z poczatku listy sciagnac?");
            ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++)
                l.usunPocz().wypisz();         //Console.WriteLine(l.usunPocz());

            Console.WriteLine("Ile elementow z konca listy sciagnac?");
            ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++)
                l.usunKon().wypisz();        //Console.WriteLine(l.usunKon());

            Console.WriteLine("Ile elementow chcesz dodac na poczatek listy?");
            ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++)
            {
                Console.WriteLine("Podaj {0} element:", i + 1);
                wart = int.Parse(Console.ReadLine());
                l.dodajNaPocz(wart);
            }

            Console.WriteLine("Ile elementow z konca listy sciagnac?");
            ile = int.Parse(Console.ReadLine());

            for (int i = 0; i < ile; i++)
                l.usunKon().wypisz();        //Console.WriteLine(l.usunKon());
        }
    }
}
