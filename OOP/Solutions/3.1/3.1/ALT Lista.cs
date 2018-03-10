using System;

namespace ListaNamespace {
    public class Lista<T> {
        static Lista<T> pocz;
        static Lista<T> kon;

        T wart;
        Lista<T> nast;
        Lista<T> poprz;

        public Lista(T inicj) {
            pocz = this;
            kon = this;

            wart = inicj;
            nast = null;
            poprz = null;
        }

        Lista(T wart, bool naPocz) {
            this.wart = wart;

            if (naPocz) {
                this.nast = pocz;
                this.poprz = null;

                pocz = this;
            }
            else {
                this.nast = null;
                this.poprz = kon;

                kon = this;
            }
        }

        public void dodajNaPocz(T e) {
            pocz.poprz = new Lista<T>(e, true);
        }

        public void dodajNaKon(T e) {
            kon.nast = new Lista<T>(e, false);
        }

        public T usunPocz() {
            T temp = pocz.wart;
            pocz = pocz.nast;
            return temp;
        }

        public T usunKon() {
            T temp = kon.wart;
            kon = kon.poprz;
            return temp;
        }
    }
}