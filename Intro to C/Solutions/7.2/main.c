// 7.2.cpp : Defines the entry point for the console application.
//

#include <stdio.h>

typedef struct ulamek {
	int x, y;
} ULAMEK;

int nwd(int a, int b) {
	int c;

	while (b != 0) {
		c = a % b;
		a = b;
		b = c;
	}

	return a;
}

struct ulamek utworz(int licznik, int mianownik) {
	ULAMEK ulamek;
	ulamek.x = licznik;
	ulamek.y = mianownik;
	return ulamek;
}

struct ulamek suma(struct ulamek a, struct ulamek b) {
	ULAMEK ulamek;
	a.x *= b.y;
	b.x *= a.y;
	ulamek.x = a.x + b.x;
	ulamek.y = a.y * b.y;
	return ulamek;
}

struct ulamek roznica(struct ulamek a, struct ulamek b) {
	ULAMEK ulamek;
	a.x *= b.y;
	b.x *= a.y;
	ulamek.x = a.x - b.x;
	ulamek.y = a.y * b.y;
	return ulamek;
}

struct ulamek iloczyn(struct ulamek a, struct ulamek b) {
	ULAMEK ulamek;
	ulamek.x = a.x * b.x;
	ulamek.y = a.y * b.y;
	return ulamek;
}

struct ulamek iloraz(struct ulamek a, struct ulamek b) {
	ULAMEK ulamek;
	ulamek.x = a.x * b.y;
	ulamek.y = a.y * b.x;
	return ulamek;
}

struct ulamek uprosc(struct ulamek a) {
	int dzielnik = nwd(a.x, a.y);
	a.x /= dzielnik;
	a.y /= dzielnik;
	return a;
}

void wypisz(struct ulamek a) {
	a = uprosc(a);

	if (a.x == 0 || a.y == 1)
		printf("%d\n", a.x);
	else if (a.y == -1)
		printf("%d\n", -a.x);
	else if (a.y < 0)
		printf("%d/%d\n", -a.x, -a.y);
	else
		printf("%d/%d\n", a.x, a.y);
}

int main()
{
	int x1, x2, y1, y2;
	ULAMEK a, b;
	printf("Podaj licznik 1 ulamka: ");
	scanf("%d", &x1);
	printf("Podaj mianownik 1 ulamka: ");
	scanf("%d", &y1);
	printf("Podaj licznik 2 ulamka: ");
	scanf("%d", &x2);
	printf("Podaj mianownik 2 ulamka: ");
	scanf("%d", &y2);
	a = utworz(x1, y1);
	b = utworz(x2, y2);
	wypisz(a);
	wypisz(b);
	wypisz(suma(a, b));
	wypisz(roznica(a, b));
	wypisz(iloczyn(a, b));
	wypisz(iloraz(a, b));

    return 0;
}

