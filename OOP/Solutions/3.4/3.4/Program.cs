using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using WiMNamespace;

namespace _3._4 {
    class Program {
        static void Main(string[] args) {
            float x, y;

            Console.WriteLine("Podaj wspolrzedna x pierwszego wektora: ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Podaj wspolrzedna y pierwszego wektora: ");
            y = int.Parse(Console.ReadLine());
            Wektor w1 = new Wektor(x, y);
            
            Console.WriteLine("Podaj wspolrzedna x pierwszego wektora: ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Podaj wspolrzedna y pierwszego wektora: ");
            y = int.Parse(Console.ReadLine());
            Wektor w2 = new Wektor(x, y);
            
            Console.WriteLine("Wynik dodawania wektorow: ");
            (w1 + w2).print();
            Console.WriteLine("Iloczyn skalarny wektorow: {0}", w1 * w2);

            Console.WriteLine("Przez jaka liczbe pomnozyc pierwszy wektor? ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Wynik mnozenia: ");
            (w1 * x).print();

            Console.WriteLine("Podaj wspolrzedna x pierwszego wektora do drugiej macierzy: ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Podaj wspolrzedna y pierwszego wektora do drugiej macierzy: ");
            y = int.Parse(Console.ReadLine());
            Wektor w3 = new Wektor(x, y);

            Console.WriteLine("Podaj wspolrzedna x drugiego wektora do drugiej macierzy: ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Podaj wspolrzedna y drugiego wektora do drugiej macierzy: ");
            y = int.Parse(Console.ReadLine());
            Wektor w4 = new Wektor(x, y);

            Macierz m1 = new Macierz(w1, w2);
            Macierz m2 = new Macierz(w3, w4);

            Console.WriteLine("Wynik dodawania macierzy:");
            (m1 + m2).print();
            Console.WriteLine("Wynik mnozenia macierzy:");
            (m1 * m2).print();

            Console.WriteLine("Podaj wspolrzedna x wektora do pomnozenia przez pierwsza macierz: ");
            x = int.Parse(Console.ReadLine());
            Console.WriteLine("Podaj wspolrzedna y wektora do pomnozenia przez pierwsza macierz: ");
            y = int.Parse(Console.ReadLine());
            Wektor w5 = new Wektor(x, y);

            Console.WriteLine("Wynik mnozenia: ");
            (m1 * w5).print();
        }
    }
}
