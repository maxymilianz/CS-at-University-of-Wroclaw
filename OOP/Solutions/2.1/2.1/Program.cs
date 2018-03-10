using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _2._1 {
    class Program {
        static void Main(string[] args) {
            int amount;
            IntStream s = new IntStream();
            PrimeStream ps = new PrimeStream();
            RandomStream rs = new RandomStream();
            RandomWordStream rws = new RandomWordStream();

            Console.WriteLine("Ile kolejnych liczb naturalnych wyswietlic?");
            amount = int.Parse(Console.ReadLine());
            for (int i = 0; i < amount; i++)
                Console.WriteLine(s.next());
            Console.WriteLine("EOS == {0}", s.eos());

            Console.WriteLine("Ile kolejnych liczb pierwszych wyswietlic?");
            amount = int.Parse(Console.ReadLine());
            for (int i = 0; i < amount; i++)
                Console.WriteLine(ps.next());
            Console.WriteLine("EOS == {0}", ps.eos());

            Console.WriteLine("Ile losowych liczb wyswietlic?");
            amount = int.Parse(Console.ReadLine());
            for (int i = 0; i < amount; i++)
                Console.WriteLine(rs.next());
            Console.WriteLine("EOS == {0}", rs.eos());

            Console.WriteLine("Ile losowych stringow wyswietlic?");
            amount = int.Parse(Console.ReadLine());
            for (int i = 0; i < amount; i++)
                Console.WriteLine(rws.next());
            Console.WriteLine("EOS == {0}", rws.eos());
        }
    }

    class IntStream {
        protected int a = 0;

        virtual public int next() {
            return a++;
        }

        virtual public bool eos() {
            return a == System.Int32.MaxValue || a < 0 ? true : false;
        }

        virtual public void reset() {
            a = 0;
        }
    }

    class PrimeStream : IntStream {
        override public int next() {
            if (a == 0)
                a = 2;
            else {
                bool found = false;

                while (!found) {
                    a++;
                    found = true;

                    for (int i = 2; i < a; i++)
                        if (a % i == 0)
                            found = false;
                }
            }

            return a;
        }

        override public void reset() {
            a = 2;
        }
    }

    class RandomStream : IntStream {
        Random r = new Random();

        override public int next() {
            return r.Next();
        }

        override public bool eos() {
            return false;
        }

        override public void reset() { }
    }

    class RandomWordStream {
        int p;
        PrimeStream ps = new PrimeStream();
        RandomStream rs = new RandomStream();

        public string next() {
            p = ps.next();
            StringBuilder b = new StringBuilder();

            for (int i = 0; i < p; i++) {
                b.Append(Convert.ToChar('A' + (rs.next() % ('Z' - 'A'))));
            }

            return b.ToString();
        }

        public bool eos() {
            return p == System.Int32.MaxValue || p < 0 ? true : false;
        }

        public void reset() {
            p = 0;
            ps.reset();
        }
    }
}
