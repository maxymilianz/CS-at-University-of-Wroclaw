using System;

namespace WiMNamespace {
    public class Wektor {
        float x, y;

        public Wektor(float x, float y) {
            this.x = x;
            this.y = y;
        }

        public float getX() {
            return x;
        }

        public float getY() {
            return y;
        }

        public void print() {
            Console.WriteLine("{0}\t{1}", x, y);
        }

        public static Wektor operator +(Wektor w1, Wektor w2) {
            return new Wektor(w1.x + w2.x, w1.y + w2.y);
        }

        public static float operator *(Wektor w1, Wektor w2) {
            return w1.x * w2.x + w1.y * w2.y;
        }

        public static Wektor operator *(Wektor w, float f) {
            return new Wektor(w.x * f, w.y * f);
        }
    }

    public class Macierz {
        Wektor[] wektory = new Wektor[2];

        public Macierz(Wektor w1, Wektor w2) {
            wektory[0] = w1;
            wektory[1] = w2;
        }

        public void print() {
            wektory[0].print();
            wektory[1].print();
        }

        public static Macierz operator +(Macierz m1, Macierz m2) {
            return new Macierz(m1.wektory[0] + m2.wektory[0], m1.wektory[1] + m2.wektory[1]);
        }

        public static Macierz operator *(Macierz m1, Macierz m2) {
            return new Macierz(new Wektor(m1.wektory[0].getX() * m2.wektory[0].getX() + m1.wektory[0].getY() * m2.wektory[1].getX(),
                m1.wektory[0].getX() * m2.wektory[0].getY() + m1.wektory[0].getY() * m2.wektory[1].getY()),
                new Wektor(m1.wektory[1].getX() * m2.wektory[0].getX() + m1.wektory[1].getY() * m2.wektory[1].getX(),
                m1.wektory[1].getX() * m2.wektory[0].getY() + m1.wektory[1].getY() * m2.wektory[1].getY()));
        }

        public static Wektor operator *(Macierz m, Wektor w) {
            return new Wektor(w * m.wektory[0], w * m.wektory[1]);
        }
    }
}