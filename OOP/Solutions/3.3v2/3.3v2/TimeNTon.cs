using System;
using System.Collections.Generic;

namespace TNTNamespace
{
    public class Elem<T>
    {
        bool czyNull = false;
        T wart;
        public Elem<T> nast;
        Elem<T> poprz;

        public T wezWart()
        {
            return wart;
        }

        public Elem<T> this[int indeks] {
            get {
                if (indeks == 0)
                    return this;
                else
                    return this.nast[indeks - 1];
            }
        }

        public Elem()
        {
            this.czyNull = true;
            this.nast = null;
            this.poprz = null;
        }

        public Elem(T wart)
        {
            this.wart = wart;
            this.nast = null;
            this.poprz = null;
        }

        public void dodajPrzed(T wart)
        {
            this.poprz = new Elem<T>(wart);
            this.poprz.nast = this;
            this.poprz.poprz = null;
        }

        public void dodajZa(T wart)
        {
            this.nast = new Elem<T>(wart);
            this.nast.nast = null;
            this.nast.poprz = this;
        }

        public Elem<T> wezPoprz()
        {
            return this.poprz;
        }

        public Elem<T> wezNast()
        {
            return this.nast;
        }

        public void wypisz()
        {
            if (!czyNull)
                Console.WriteLine(wart);
            else
                Console.WriteLine("Nie ma takiego elementu!");
        }
    }

    public class Lista<T>
    {
        public int ile = 0;
        public Elem<T> pocz;
        Elem<T> kon;

        public Lista()
        {
            pocz = null;
            kon = null;
        }

        public Lista(T inicj)
        {
            ile++;
            pocz = new Elem<T>(inicj);
            kon = pocz;
        }

        public void dodajNaPocz(T e)
        {
            ile++;

            if (pocz != null)
            {
                pocz.dodajPrzed(e);
                pocz = pocz.wezPoprz();
            }
            else
            {
                pocz = new Elem<T>(e);
                kon = pocz;
            }
        }

        public void dodajNaKon(T e)
        {
            ile++;

            if (kon != null)
            {
                kon.dodajZa(e);
                kon = kon.wezNast();
            }
            else
            {
                kon = new Elem<T>(e);
                pocz = kon;
            }
        }

        public Elem<T> usunPocz()
        {
            Elem<T> temp = pocz;

            if (this != null)
            {
                ile--;

                if (pocz != kon)
                    pocz = pocz.wezNast();
                else
                {
                    pocz = null;
                    kon = null;
                }
            }

            if (temp != null)
                return temp;
            else
                return new Elem<T>();
        }

        public Elem<T> usunKon()
        {
            Elem<T> temp = kon;

            if (this != null)
            {
                ile--;

                if (pocz != kon)
                    kon = kon.wezPoprz();
                else
                {
                    pocz = null;
                    kon = null;
                }
            }

            if (temp != null)
                return temp;
            else
                return new Elem<T>();
        }
    }

    public sealed class TimeNTon
    {
        const int N = 3;

        public static DateTime start = new DateTime(2017, 3, 17, 8, 0, 0);
        //static DateTime start = DateTime.Now.AddHours(-1);
        static DateTime end = start.AddHours(2);

        static int i = -1;
        static Lista<TimeNTon> instances = new Lista<TimeNTon>();
        int id;

        TimeNTon()
        {
            id = -1;
        }

        TimeNTon(int i)
        {
            id = i;
        }

        public int getId()
        {
            return id;
        }

        public static TimeNTon instance()
        {
            if (DateTime.Now.CompareTo(start) == 1 && DateTime.Now.CompareTo(end) == -1)
            {
                if (instances.ile == TimeNTon.N)
                {
                    i++;
                    if (i == TimeNTon.N)
                        i = 0;

                    Elem<TimeNTon> temp = instances.pocz;
                    for (int j = 0; j < i; j++)
                        temp = temp.nast;

                    return temp.wezWart();
                }
                else
                {
                    instances.dodajNaKon(new TimeNTon(instances.ile));

                    Elem<TimeNTon> temp = instances.pocz;
                    for (int i = 0; i < instances.ile - 1; i++)
                        temp = temp.nast;

                    return temp.wezWart();
                }
            }
            else
            {
                if (instances.ile == 0)
                    instances.dodajNaKon(new TimeNTon());
                

                return instances.pocz.wezWart();
            }
        }
    }
}