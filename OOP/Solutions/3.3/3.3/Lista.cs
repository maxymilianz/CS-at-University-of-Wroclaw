using System;

namespace ListaNamespace {
    public class Elem<T> {
        bool czyNull = false;
        T wart;
        Elem<T> nast;
        Elem<T> poprz;

        public Elem()
        {
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

        public Elem<T> wezPoprz() {
            return this.poprz;
        }

        public Elem<T> wezNast() {
            return this.nast;
        }

        public void wypisz() {
            if (!czyNull)
                Console.WriteLine(wart);
            else
                Console.WriteLine("Nie ma takiego elementu!");
        }
    }

    public class Lista<T> {
        Elem<T> pocz;
        Elem<T> kon;

        public Lista(T inicj) {
            pocz = new Elem<T>(inicj);
            kon = pocz;
        }

        public void dodajNaPocz(T e) {
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

        public void dodajNaKon(T e) {
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

        public Elem<T> usunKon()
        {
            Elem<T> temp = kon;

            if (this != null)
            {
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
}